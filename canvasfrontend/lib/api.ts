export type ApiOptions = RequestInit & { json?: any };

function backend() {
  return process.env.NEXT_PUBLIC_BACKEND_URL || process.env.BACKEND_URL || "";
}

export async function api(path: string, options: ApiOptions = {}) {
  const url = `${backend()}${path}`;
  const { json, headers, ...rest } = options;
  const init: RequestInit = {
    credentials: "include",
    headers: {
      ...(json ? { "Content-Type": "application/json" } : {}),
      ...(headers || {}),
    },
    ...rest,
    body: json ? JSON.stringify(json) : rest.body,
  };
  const res = await fetch(url, init);
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`API ${res.status}: ${text}`);
  }
  const ct = res.headers.get("content-type") || "";
  if (ct.includes("application/json")) return res.json();
  return res.text();
}

export const get = (path: string, options?: ApiOptions) => api(path, { ...(options || {}), method: "GET" });
export const post = (path: string, json?: any, options?: ApiOptions) => api(path, { ...(options || {}), method: "POST", json });
export const del = (path: string, options?: ApiOptions) => api(path, { ...(options || {}), method: "DELETE" });
export const put = (path: string, json?: any, options?: ApiOptions) => api(path, { ...(options || {}), method: "PUT", json });
