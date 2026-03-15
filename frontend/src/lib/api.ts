const BASE_URL = "http://localhost:8001";
const TENANT_ID = "20d3debb-adcd-48b3-89e9-e49abfb6fbda";

export interface Lead {
  id: string;
  whatsapp_number: string;
  intent: string;
  budget: string;
  zone: string;
  score: string;
  created_at: string;
  interactions?: Interaction[];
}

export interface Interaction {
  id: string;
  type: "user" | "ai";
  message: string;
  timestamp: string;
}

export interface Metrics {
  total_leads: number;
  hot_leads: number;
  warm_leads: number;
  cold_leads: number;
}

class ApiError extends Error {
  constructor(message: string, public status?: number) {
    super(message);
    this.name = "ApiError";
  }
}

async function fetchApi<T>(endpoint: string): Promise<T> {
  const separator = endpoint.includes("?") ? "&" : "?";
  const url = `${BASE_URL}${endpoint}${separator}tenant_id=${TENANT_ID}`;
  
  try {
    const res = await fetch(url);
    if (!res.ok) throw new ApiError(`Server error: ${res.status}`, res.status);
    return res.json();
  } catch (err) {
    if (err instanceof ApiError) throw err;
    throw new ApiError("Cannot connect to server. Please check your connection.");
  }
}

export const api = {
  getMetrics: () => fetchApi<Metrics>("/api/v1/leads/metrics"),
  getLeads: () => fetchApi<Lead[]>("/api/v1/leads"),
  getLead: (id: string) => fetchApi<Lead>(`/api/v1/leads/${id}`),
};
