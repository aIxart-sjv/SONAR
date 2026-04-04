import type{ NetworkEvent } from "../types/event";

export async function fetchEvents(): Promise<NetworkEvent[]> {
  const res = await fetch("http://localhost:8000/events");
  return res.json();
}