import { useEventsStore } from "../../store/useEventsStore";
import type { NetworkEvent } from "../../types/event";

function generateAlerts(events: NetworkEvent[]) {
  const map: Record<string, number> = {};

  for (const e of events) {
    if (!e.attack || e.attack === "Benign") continue;
    map[e.attack] = (map[e.attack] || 0) + 1;
  }

  return Object.entries(map)
    .map(([attack, count]) => ({
      attack,
      count,
      severity:
        count > 20
          ? "high"
          : count > 10
          ? "medium"
          : "low",
    }))
    .sort((a, b) => b.count - a.count);
}

export default function AlertsPanel() {
  const events = useEventsStore((s) => s.events);
  const attackFilter = useEventsStore((s) => s.attackFilter);
  const setAttackFilter = useEventsStore(
    (s) => s.setAttackFilter
  );

  const alerts = generateAlerts(events);

  return (
    <div className="h-full overflow-y-auto">
      <h2 className="text-sm text-gray-400 mb-3">
        Alerts
      </h2>

      {alerts.length === 0 && (
        <div className="text-gray-500 text-sm">
          No threats detected
        </div>
      )}

      <div className="space-y-2">
        {alerts.map((a, i) => {
          const active = attackFilter === a.attack;

          return (
            <div
              key={i}
              onClick={() => setAttackFilter(a.attack)}
              className={`flex justify-between px-3 py-2 rounded-lg cursor-pointer
                ${
                  active
                    ? "bg-red-900/40 border border-red-500/30"
                    : "bg-[#0f172a] hover:bg-[#1f2937]"
                }`}
            >
              <span className="text-sm text-white">
                {a.attack}
              </span>

              <span className="text-xs text-gray-400">
                {a.count}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}