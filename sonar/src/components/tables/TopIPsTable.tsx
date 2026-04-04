import { useEventsStore } from "../../store/useEventsStore";
import type { NetworkEvent } from "../../types/event";

function generateIPStats(events: NetworkEvent[]) {
  const map: Record<string, number> = {};

  for (const e of events) {
    if (!e.src_ip) continue;
    map[e.src_ip] = (map[e.src_ip] || 0) + 1;
  }

  return Object.entries(map)
    .map(([ip, count]) => ({
      ip,
      count,
      severity:
        count > 50
          ? "high"
          : count > 20
          ? "medium"
          : "low",
    }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 10);
}

export default function TopIPsTable() {
  const events = useEventsStore((s) => s.events);
  const ipFilter = useEventsStore((s) => s.ipFilter);
  const setIpFilter = useEventsStore((s) => s.setIpFilter);

  const stats = generateIPStats(events);

  return (
    <div>
      <h2 className="text-sm text-gray-400 mb-3">
        Top Source IPs
      </h2>

      <div className="space-y-2">
        {stats.map((s, i) => {
          const active = ipFilter === s.ip;

          return (
            <div
              key={i}
              onClick={() => setIpFilter(s.ip)}
              className={`flex justify-between px-3 py-2 rounded-lg cursor-pointer
                ${
                  active
                    ? "bg-blue-900/40 border border-blue-500/30"
                    : "bg-[#0f172a] hover:bg-[#1f2937]"
                }`}
            >
              <span className="text-sm text-gray-300">
                {s.ip}
              </span>

              <span className="text-xs text-gray-400">
                {s.count}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
}