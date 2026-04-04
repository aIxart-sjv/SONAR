import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

type DataItem = {
  name: string;
  value: number;
};

type Props = {
  title: string;
  data: DataItem[];
};

export default function BarCard({ title, data }: Props) {
  return (
    <div className="bg-[#111827] p-4 rounded-xl h-[260px] flex flex-col">
      <h2 className="text-sm text-gray-400 mb-3">{title}</h2>

      <div className="flex-1">
        <ResponsiveContainer>
          <BarChart data={data}>
            <XAxis
              dataKey="name"
              stroke="#9ca3af"
              tick={{ fontSize: 12 }}
            />

            <YAxis stroke="#9ca3af" />

            <Tooltip
              contentStyle={{
                backgroundColor: "#0f172a",
                border: "none",
                borderRadius: "8px",
              }}
            />

            <Bar
              dataKey="value"
              fill="#60a5fa"
              radius={[6, 6, 0, 0]}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}