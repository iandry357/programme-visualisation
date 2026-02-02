/**
 * Google Analytics helper
 * Track des événements personnalisés
 */

declare global {
  interface Window {
    gtag?: (
      command: string,
      targetId: string,
      config?: Record<string, any>
    ) => void;
  }
}

/**
 * Track le téléchargement du PDF
 */
export function trackPdfDownload(concertId: number, concertTitle: string) {
  if (typeof window !== "undefined" && window.gtag) {
    window.gtag("event", "pdf_download", {
      event_category: "engagement",
      event_label: concertTitle,
      concert_id: concertId,
    });
  }
}

/**
 * Track la navigation entre pages du concert
 */
export function trackPageNavigation(
  concertId: number,
  pageNumber: number,
  method: "keyboard" | "swipe" | "button" | "thumbnail"
) {
  if (typeof window !== "undefined" && window.gtag) {
    window.gtag("event", "page_navigation", {
      event_category: "engagement",
      event_label: `Page ${pageNumber}`,
      concert_id: concertId,
      page_number: pageNumber,
      navigation_method: method,
    });
  }
}