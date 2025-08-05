import { useEffect, useState } from "react";

import { useCurrentReadingStore } from "@/core/presentation/stores/currentReadingStore";
import MainLayout from "@/core/presentation/layouts/MainLayout";
import { adaptRawDataByIndexGroup } from "@/core/presentation/adapters/adpterRawDataByIndex";
import { ChartCard } from "./components/ChartCard";

// ✅ Página principal que gestiona el polling
export default function Page() {
  const { multiRawData, startPollingForTable, stopPollingForTable } =
    useCurrentReadingStore();

  const equipments = ["top-drive", "drawworks"];
  const mudPumps = ["mud-pump1", "mud-pump2", "mud-pump3"];
  const generatos = [
    "generator1",
    "generator2",
    "generator3",
    "generator4",
    "generator5",
  ];
  const fgnerators = [
    "fgenerador1_data",
    "fgenerador2_data",
    "fgenerador3_data",
    "fgenerador4_data",
    "fgenerador5_data",
    "fgenerador6_data",
    "fgenerador7_data",
  ];

  // Inicia polling al montar el componente
  useEffect(() => {
    equipments.forEach((table) => startPollingForTable(table));
    mudPumps.forEach((table) => startPollingForTable(table));
    generatos.forEach((table) => startPollingForTable(table));
    fgnerators.forEach((table) => startPollingForTable(table));
    return () => {
      equipments.forEach((table) => stopPollingForTable(table));
      mudPumps.forEach((table) => stopPollingForTable(table));
      generatos.forEach((table) => stopPollingForTable(table));
      fgnerators.forEach((table) => stopPollingForTable(table));
    };
  }, []);

  // datos crudos
  const rawTopDrive = multiRawData["top-drive"]?.data ?? null;
  const rawDrawworks = multiRawData["drawworks"]?.data ?? null;

  // datos agrupados mediante el adapter
  const groupedTopDrive = adaptRawDataByIndexGroup(rawTopDrive);
  const groupedDawworks = adaptRawDataByIndexGroup(rawDrawworks);

  // ✅ Para cada subequipo creas rawData y groupedData
  const mudPumpsReadings = mudPumps.map((table) => {
    const rawData = multiRawData[table]?.data ?? null;
    const groupedData = adaptRawDataByIndexGroup(rawData);
    return { table, rawData, groupedData };
  });

  // ✅ Para cada subequipo creas rawData y groupedData
  const generatorsReadings = generatos.map((table) => {
    const rawData = multiRawData[table]?.data ?? null;
    const groupedData = adaptRawDataByIndexGroup(rawData);
    return { table, rawData, groupedData };
  });

  // ✅ Para cada subequipo creas rawData y groupedData
  const fuelGeneratorsReadings = fgnerators.map((table) => {
    const rawData = multiRawData[table]?.data ?? null;
    const groupedData = adaptRawDataByIndexGroup(rawData);
    return { table, rawData, groupedData };
  });

  return (
    <MainLayout title="Dashboard">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <ChartCard
          equipmentName="Top Drive"
          equipmentImage="/images/top-drive-icon.png"
          lineColor="#ff9800"
          onlyEquipmentReadings={groupedTopDrive}
        />
        <ChartCard
          equipmentName="Drawworks"
          equipmentImage="/images/drawworks-icon.png"
          lineColor="#2196f3"
          onlyEquipmentReadings={groupedDawworks}
        />
        <ChartCard
          equipmentName="Mud Pumps"
          equipmentImage="/images/mud-pump-icon.png"
          lineColor="#e91e63"
          multipleEquipmentReadings={mudPumpsReadings}
        />
        <ChartCard
          equipmentName="Generators"
          equipmentImage="/images/mud-pump-icon.png"
          lineColor="#4caf50"
          multipleEquipmentReadings={generatorsReadings}
        />
        <ChartCard
          equipmentName="Diesel Generators"
          equipmentImage="/images/generator-icon.png"
          lineColor="#ff7ca3"
          multipleEquipmentReadings={fuelGeneratorsReadings}
        />
        <ChartCard
          equipmentName="Surface Parameters"
          equipmentImage="/images/generator-icon.png"
          lineColor="#009688"
          multipleEquipmentReadings={fuelGeneratorsReadings}
        />
      </div>
    </MainLayout>
  );
}
