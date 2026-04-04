import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Tooltip,
} from "recharts";

type DataItem = {
  name: string;
  value: number;
};

type Props = {
  title: string;
  data: DataItem[];
};

const COLORS = ["#60a5fa", "#f87171", "#facc15", "#34d399", "#a78bfa"];

export default function DonutCard({ title, data }: Props) {
  const total = data.reduce((sum, d) => sum + d.value, 0);

  return (
    <div className="bg-[#111827] p-4 rounded-xl h-[260px] flex flex-col">
      <h2 className="text-sm text-gray-400 mb-2">{title}</h2>

      <div className="flex-1 relative">
        <ResponsiveContainer>
          <PieChart>
            <Pie
              data={data}
              dataKey="value"
              nameKey="name"
              innerRadius={55}
              outerRadius={85}
              paddingAngle={3}
            >
              {data.map((_, i) => (
                <Cell key={i} fill={COLORS[i % COLORS.length]} />
              ))}
            </Pie>

            <Tooltip
              contentStyle={{
                backgroundColor: "#0f172a",
                border: "none",
                borderRadius: "8px",
              }}
            />
          </PieChart>
        </ResponsiveContainer>

        {/* 🔥 CENTER TEXT (this is why donut > pie) */}
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-sm text-gray-300">{total}</span>
        </div>
      </div>
    </div>
  );
}