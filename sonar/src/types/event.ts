export type NetworkEvent = {
  attack: string;
  service: string;
  layer: string;
  port: number;
  packets: number;
  anomaly: boolean;
  src_ip: string;
  timestamp: string;
};