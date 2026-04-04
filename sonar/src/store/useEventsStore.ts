import { create } from "zustand";
import type { NetworkEvent } from "../types/event";

type State = {
  events: NetworkEvent[];

  attackFilter: string | null;
  ipFilter: string | null;

  addEvents: (newEvents: NetworkEvent[]) => void;

  setAttackFilter: (attack: string | null) => void;
  setIpFilter: (ip: string | null) => void;

  clearFilters: () => void;
};

export const useEventsStore = create<State>((set) => ({
  events: [],

  attackFilter: null,
  ipFilter: null,

  addEvents: (newEvents) =>
    set((state) => ({
      events: [...newEvents, ...state.events].slice(0, 1000),
    })),

  setAttackFilter: (attack) =>
    set((state) => ({
      attackFilter:
        state.attackFilter === attack ? null : attack,
    })),

  setIpFilter: (ip) =>
    set((state) => ({
      ipFilter: state.ipFilter === ip ? null : ip,
    })),

  clearFilters: () =>
    set({
      attackFilter: null,
      ipFilter: null,
    }),
}));