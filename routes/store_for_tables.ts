// 🛠️ Zustand: para crear un store global y reactivo
import { create } from "zustand";

// 🧠 RxJS: para manejar programación reactiva y polling periódico
import {
  BehaviorSubject, // mantiene el nombre actual de la tabla como observable
  interval, // genera valores periódicos (cada 3s en este caso)
  switchMap, // permite cambiar al observable de ejecución de la petición
  withLatestFrom, // combina el intervalo con el valor más reciente del nombre de tabla
  Subscription, // para manejar y cancelar la suscripción manualmente
  from, // convierte una promesa en observable (para usar con switchMap)
} from "rxjs";

// 📦 Lógica de negocio y acceso a datos
import { GetCurrentReadings } from "../../domain/usecases/getCurrentReadings";
import { CurrentReadingRepositoryImpl } from "../../data/repositories/currentReadingsRepositoryimpl";
import { ChannelAPI } from "../../data/datasources/channelAPI";
import { equipmentConfig } from "../../domain/config/equpmentConfig";
import { useEquipmentLayoutStore } from "./useEquipmentLayoutStore";

// 🔌 Instancia del caso de uso, que internamente accede al repositorio y al datasource
const usecase = new GetCurrentReadings(
  new CurrentReadingRepositoryImpl(new ChannelAPI())
);

// 🧪 Observable reactivo que almacena el nombre de la tabla seleccionada
const tableName$ = new BehaviorSubject<string>("");

// 📂 Multi-polling controllers
// Nuevo estado auxiliar para polling de otras tablas en simultaneo
const multiPollingControllers = new Map<
  string,
  {
    rawData: any;
    subject: BehaviorSubject<string>;
    subscription: Subscription | null;
  }
>();

// 🧬 Tipo del Zustand store
type Store = {
  rawData: any; // datos en crudo
  multiRawData: Record<string, any>; // 🚨 nuevo estado para rawData de múltiples tablas

  // todo: borrar.
  selectedTable: string; // tabla actual
  setTable: (table: string) => void; // cambia la tabla actual
  startPolling: () => void; // inicia polling cada 3s
  stopPolling: () => void; // detiene el polling
  setSystem: (system: string) => void; // cambia el sistem seleccionado (lubrication, electric...)
  setEquipmentNumber: (num: number) => void; // cambia el sub equipo para los equipos con varias tablas (fgenerators)
  // todo: borrar.

  // Nuevas funciones para multiples tablas
  resetReadings: () => void; // resetea las readings al cambiar de page
  startPollingForTable: (table: string) => void; // inicia el polling por tabla para el multipolling
  stopPollingForTable: (table: string) => void; // detiene el polling por tabla paa el multipolling
  getRawDataForTable: (table: string) => any | null; // 🚨 nueva función para obtener las readings crudas por tabla
};

// Nuevos estados para manejar de manera dinamica el equipò seleccionado
let selectedSystem = "lubrication";
let selectedEquipmentNumber = 1;

// 🔁 Guardamos la suscripción activa para poder detenerla manualmente luego
let pollingSubscription: Subscription | null;

// 🧠 Creamos el Zustand store
export const useCurrentReadingStore = create<Store>((set) => ({
  rawData: {}, // estado inicial sin lecturas (crudas)
  multiRawData: {}, // 🚨 nuevo estado para obtener readings crudas de multiples tablas

  // Todo: BORRAR (Metodos sin utilizar)
  selectedTable: "fgenerador1_data", // valor inicial por defecto
  // ✅ Cambia la tabla actual
  setTable: (table) => {
    // para setear una nueva tabla obtenermos el estado con la tabla previa y la limpiamos
    useCurrentReadingStore.getState().resetReadings();
    tableName$.next(table); // actualiza el observable tableName$
    set({ selectedTable: table }); // actualiza el estado del store
  },

  // ✅ Cambia el system actual
  setSystem: (system) => {
    selectedSystem = system;
    updateTableName();
  },

  // ✅ Cambia el numero de sub equipo actual
  setEquipmentNumber: (num) => {
    selectedEquipmentNumber = num;
    updateTableName();
  },

  // ▶️ Inicia el polling (si no está activo ya)
  startPolling: () => {
    // Verificamos si existe alguna suscripcion activa
    if (pollingSubscription) return;

    // Obtenemos la tabla emitida en el observable
    const table = tableName$.value;

    // 🚀 Ejecuta una lectura INICIAL inmediata antes del intervalo
    from(usecase.execute(table)).subscribe((raw) => {
      set({ rawData: raw, selectedTable: table });
      console.log("📦 Raw JSON inicial:", JSON.stringify(raw, null, 2));
    });

    // ⏱️ Luego comienza el polling cada 3 segundos
    const polling$ = interval(3000).pipe(
      withLatestFrom(tableName$),
      switchMap(([_, t]) => from(usecase.execute(t)))
    );

    pollingSubscription = polling$.subscribe((raw) => {
      set({ rawData: raw, selectedTable: tableName$.value });
    });
  },

  // ⏹️ Detiene el polling (si está activo)
  stopPolling: () => {
    pollingSubscription?.unsubscribe();
    pollingSubscription = null;
  },
  // Todo: Borrar.

  // 🆕 Multi-Polling: inicia polling para unta tabla adicional
  startPollingForTable: (table) => {
    if (multiPollingControllers.has(table)) return;
    const subject = new BehaviorSubject<string>(table);
    const controller = {
      rawData: {},
      subject,
      subscription: null as Subscription | null,
    };

    const polling$ = interval(3000).pipe(
      withLatestFrom(subject),
      switchMap(([_, t]) => from(usecase.execute(t)))
    );

    controller.subscription = polling$.subscribe((raw) => {
      controller.rawData = raw;
      set((state) => ({
        multiRawData: { ...state.multiRawData, [table]: raw },
      }));
    });

    multiPollingControllers.set(table, controller);
  },

  // 🆕 Multi-Polling: detiene polling para unta tabla adicional
  stopPollingForTable: (table) => {
    const controller = multiPollingControllers.get(table);
    if (!controller) return;
    controller.subscription?.unsubscribe();
    multiPollingControllers.delete(table);
    set((state) => {
      const newData = { ...state.multiRawData };
      delete newData[table];
      return { multiRawData: newData };
    });
  },

  // ✅ Obtiene las readings crudas de una tabla
  getRawDataForTable: (table) => {
    return multiPollingControllers.get(table)?.rawData ?? null;
  },

  // 🧹 limpia las variables agrupadas, en crudo y detiene todos los polling activos
  resetReadings: () => {
    // Detener polling general
    pollingSubscription?.unsubscribe();
    pollingSubscription = null;

    // Detener y limpiar cada polling individual
    multiPollingControllers.forEach((controller, table) => {
      controller.subscription?.unsubscribe();
    });
    multiPollingControllers.clear();

    // Limpiar todos los datos del estado
    set({
      rawData: {},
      multiRawData: {},
      // readings: {}, // Si usas lecturas agrupadas, también límpialas aquí
    });
  },
}));

// Todo: borrarjaj
// 🔄 Actualiza la tabla principal segun el equipo y sistema seleccionados
function updateTableName() {
  const { equipment } = useEquipmentLayoutStore.getState();
  const config = equipmentConfig[equipment];

  if (!config) return;

  const baseName = config.hasMultiple
    ? `${config.prefix}${selectedEquipmentNumber}`
    : config.prefix;

  const tableName = config.hasDataSuffix ? `${baseName}_data` : baseName;

  // Limpiar los datos antes de actualizar la tabla
  useCurrentReadingStore.getState().resetReadings();
  tableName$.next(tableName);
}
