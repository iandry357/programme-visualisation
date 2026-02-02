import { Concert } from "@/types/concert";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// export async function getConcert(id: number): Promise<Concert> {
//   const response = await fetch(`${API_URL}/api/concerts/${id}`, {
//     cache: "no-store",
//   });

//   if (!response.ok) {
//     throw new Error(`Failed to fetch concert: ${response.statusText}`);
//   }

//   return response.json();
// }

export async function getConcert(id: number, signal?: AbortSignal): Promise<Concert> {
  const response = await fetch(`${API_URL}/api/concerts/${id}`, {
    cache: "no-store",
    signal, // Ajout du signal pour timeout
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch concert: ${response.statusText}`);
  }

  return response.json();
}

export function getPagePngUrl(concertId: number, pageNumber: number): string {
  return `${API_URL}/api/concerts/${concertId}/pages/${pageNumber}/png`;
}

export function getPdfUrl(concertId: number): string {
  return `${API_URL}/api/concerts/${concertId}/pdf`;
}