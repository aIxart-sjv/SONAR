// src/hooks/useEventStream.ts
import { useEffect } from "react";
import { fetchEvents } from "../services/api";
import { useEventsStore } from "../store/useEventsStore";

export function useEventStream() {
  const addEvents = useEventsStore((s) => s.addEvents);

  useEffect(() => {
    const interval = setInterval(async () => {
      const data = await fetchEvents();
      addEvents(data);
    }, 2000);

    return () => clearInterval(interval);
  }, []);
}