import { useEventsStore } from "../../store/useEventsStore";

export default function LiveTable() {
  const events = useEventsStore((s) => s.events);

  const latest = [...events].slice(-20).reverse();

  return (
    <div className="bg-[#111827] p-4 rounded-xl h-[300px] overflow-y-auto">
      <h2 className="text-sm text-gray-400 mb-3">Live Events</h2>

      <table className="w-full text-xs text-left">
        <thead className="text-gray-500 border-b border-gray-700">
          <tr>
            <th className="py-1">Time</th>
            <th>IP</th>
            <th>Attack</th>
            <th>Port</th>
          </tr>
        </thead>

        <tbody>
          {latest.map((e, i) => (
            <tr key={i} className="border-b border-gray-800">
              <td className="py-1">
                {new Date(e.timestamp).toLocaleTimeString()}
              </td>
              <td>{e.src_ip}</td>
              <td
                className={
                  e.attack !== "Benign"
                    ? "text-red-400"
                    : "text-green-400"
                }
              >
                {e.attack}
              </td>
              <td>{e.port}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}