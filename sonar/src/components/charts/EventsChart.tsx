import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
} from "recharts";
import { useEventsStore } from "../../store/useEventsStore";
import type { NetworkEvent } from "../../types/event";

type ChartData = {
  time: string;
  total: number;
  attacks: number;
  anomalies: number;
  spike?: boolean;
};

// 🔥 LOCAL TIME FORMATTER (NO UTC BS)
function formatTime(date: Date) {
  const pad = (n: number) => String(n).padStart(2, "0");

  return `${pad(date.getHours())}:${pad(date.getMinutes())}:${pad(
    date.getSeconds()
  )}`;
}

// 🔥 AGGREGATION + SPIKE DETECTION
function aggregateEvents(events: NetworkEvent[]): ChartData[] {
  const map: Record<string, ChartData> = {};

  for (const e of events) {
    const date = new Date(e.timestamp.replace("T", " "));

    // ✅ FIXED: LOCAL TIME
    const key = formatTime(date);

    if (!map[key]) {
      map[key] = {
        time: key,
        total: 0,
        attacks: 0,
        anomalies: 0,
      };
    }

    map[key].total += 1;

    if (e.attack && e.attack !== "Benign") {
      map[key].attacks += 1;
    }

    if (e.anomaly) {
      map[key].anomalies += 1;
    }
  }

  const sorted = Object.values(map).sort((a, b) =>
    a.time.localeCompare(b.time)
  );

  // 🔥 SPIKE DETECTION (2x jump)
  for (let i = 1; i < sorted.length; i++) {
    const prev = sorted[i - 1].total;
    const curr = sorted[i].total;

    if (prev > 0 && curr > prev * 2) {
      sorted[i].spike = true;
    }
  }

  return sorted.slice(-60);
}

export default function EventsChart() {
  const events = useEventsStore((s) => s.events);
  const attackFilter = useEventsStore((s) => s.attackFilter);
  const ipFilter = useEventsStore((s) => s.ipFilter);

  // 🔥 FILTER PIPELINE
  let filtered = events;

  if (attackFilter) {
    filtered = filtered.filter((e) => e.attack === attackFilter);
  }

  if (ipFilter) {
    filtered = filtered.filter((e) => e.src_ip === ipFilter);
  }

  const data = aggregateEvents(filtered);

  // 🔥 Y AXIS (SMART TICKS)
  const maxValue =
    data.length > 0
      ? Math.max(...data.map((d) => d.total))
      : 10;

  const ticks: number[] = [];
  const step = Math.max(1, Math.ceil(maxValue / 5));

  for (let i = 0; i <= maxValue + step; i += step) {
    ticks.push(i);
  }

  return (
    <div className="h-full w-full">
      <ResponsiveContainer>
        <LineChart data={data}>
          {/* 🔥 GLOW EFFECT */}
          <defs>
            <filter id="glow">
              <feGaussianBlur stdDeviation="3" result="blur" />
              <feMerge>
                <feMergeNode in="blur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
          </defs>

          <CartesianGrid stroke="#1f2937" strokeDasharray="3 3" />

          <XAxis
            dataKey="time"
            stroke="#9ca3af"
            tick={{ fontSize: 12 }}
          />

          <YAxis
            stroke="#9ca3af"
            ticks={ticks}
            domain={[0, "auto"]}
          />

          <Tooltip
            contentStyle={{
              backgroundColor: "#111827",
              border: "none",
              borderRadius: "8px",
            }}
          />

          {/* 🔵 TOTAL */}
          <Line
            type="monotone"
            dataKey="total"
            stroke="#60a5fa"
            strokeWidth={2}
            dot={false}
            isAnimationActive={false}
            filter="url(#glow)"
            activeDot={(props: any) => {
              const { payload } = props;

              if (payload?.spike) {
                return (
                  <circle
                    cx={props.cx}
                    cy={props.cy}
                    r={6}
                    fill="#ef4444"
                    stroke="#fff"
                    strokeWidth={2}
                  />
                );
              }

              return (
                <circle
                  cx={props.cx}
                  cy={props.cy}
                  r={3}
                  fill="#60a5fa"
                />
              );
            }}
          />

          {/* 🔴 ATTACKS */}
          <Line
            type="monotone"
            dataKey="attacks"
            stroke="#f87171"
            strokeWidth={2}
            dot={false}
          />

          {/* 🟡 ANOMALIES */}
          <Line
            type="monotone"
            dataKey="anomalies"
            stroke="#facc15"
            strokeWidth={2}
            dot={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}