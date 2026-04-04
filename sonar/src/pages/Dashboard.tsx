import EventsChart from "../components/charts/EventsChart";
import AlertsPanel from "../components/panels/AlertsPanel";
import TopIPsTable from "../components/tables/TopIPsTable";
import LiveTable from "../components/tables/LiveTable";
import DonutCard from "../components/cards/DonutCard";
import BarCard from "../components/cards/BarCard";

import { useEventStream } from "../hooks/useEventStream";
import { useEventsStore } from "../store/useEventsStore";
import { useMemo } from "react";

export default function Dashboard() {
  useEventStream();
  const events = useEventsStore((s) => s.events);

  /* ----------------- SINGLE CARD SYSTEM ----------------- */
  const card =
    "rounded-xl p-4 " +
    "bg-gradient-to-br from-[#0f172a] to-[#020617] " +
    "shadow-[0_8px_30px_rgba(0,0,0,0.7),inset_0_1px_0_rgba(255,255,255,0.04)] " +
    "transition-all duration-200 hover:shadow-[0_12px_45px_rgba(0,0,0,0.9)]";

  /* ----------------- DONUT DATA ----------------- */

  const eventTypes = useMemo(() => {
    let benign = 0, attacks = 0, anomalies = 0;

    for (const e of events) {
      if (e.anomaly) anomalies++;
      else if (e.attack === "Benign") benign++;
      else attacks++;3
    }

    return [
      { name: "Benign", value: benign },
      { name: "Attack", value: attacks },
      { name: "Anomaly", value: anomalies },
    ];
  }, [events]);

  const services = useMemo(() => {
    const map: Record<string, number> = {};
    for (const e of events) {
      const k = e.service || "Unknown";
      map[k] = (map[k] || 0) + 1;
    }
    return Object.entries(map).map(([name, value]) => ({ name, value }));
  }, [events]);

  const layers = useMemo(() => {
    const map: Record<string, number> = {};
    for (const e of events) {
      const k = e.layer || "Unknown";
      map[k] = (map[k] || 0) + 1;
    }
    return Object.entries(map).map(([name, value]) => ({ name, value }));
  }, [events]);

  const ports = useMemo(() => {
    const map: Record<string, number> = {};
    for (const e of events) {
      const k = String(e.port ?? "Unknown");
      map[k] = (map[k] || 0) + 1;
    }
    return Object.entries(map)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5)
      .map(([name, value]) => ({ name, value }));
  }, [events]);

  /* ----------------- BAR DATA ----------------- */

  const attackBars = useMemo(() => {
    const map: Record<string, number> = {};
    for (const e of events) {
      const k = e.attack || "Unknown";
      map[k] = (map[k] || 0) + 1;
    }
    return Object.entries(map)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 6)
      .map(([name, value]) => ({ name, value }));
  }, [events]);

  const serviceBars = useMemo(() => {
    const map: Record<string, number> = {};
    for (const e of events) {
      const k = e.service || "Unknown";
      map[k] = (map[k] || 0) + 1;
    }
    return Object.entries(map)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 6)
      .map(([name, value]) => ({ name, value }));
  }, [events]);

  const portBars = useMemo(() => {
    const map: Record<string, number> = {};
    for (const e of events) {
      const k = String(e.port ?? "Unknown");
      map[k] = (map[k] || 0) + 1;
    }
    return Object.entries(map)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 6)
      .map(([name, value]) => ({ name, value }));
  }, [events]);

  /* ----------------- UI ----------------- */

  return (
    <div className="p-5 space-y-5 bg-[#020617] min-h-screen">

      {/* TOP ROW */}
      <div className="grid grid-cols-4 gap-7">
        <div className={`col-span-3 h-[340px] flex flex-col ${card}`}>
          <div className="flex-1 min-h-0">
            <EventsChart />
          </div>
        </div>

        <div className={`h-[340px] ${card}`}>
          <AlertsPanel />
        </div>
      </div>

      {/* DONUTS */}
      <div className="grid grid-cols-4 gap-7">
        <div className={card}>
          <DonutCard title="Event Types" data={eventTypes} />
        </div>

        <div className={card}>
          <DonutCard title="Services" data={services} />
        </div>

        <div className={card}>
          <DonutCard title="Layers" data={layers} />
        </div>

        <div className={card}>
          <DonutCard title="Ports" data={ports} />
        </div>
      </div>

      {/* BARS */}
      <div className="grid grid-cols-3 gap-7">
        <div className={card}>
          <BarCard title="Services" data={serviceBars} />
        </div>

        <div className={card}>
          <BarCard title="Attacks" data={attackBars} />
        </div>

        <div className={card}>
          <BarCard title="Ports" data={portBars} />
        </div>
      </div>

      {/* TABLES */}
      <div className="grid grid-cols-2 gap-7">
        <div className={card}>
          <LiveTable />
        </div>

        <div className={card}>
          <TopIPsTable />
        </div>
      </div>

    </div>
  );
}