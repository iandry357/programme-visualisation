"use client";

import { useEffect, useState } from "react";
import { PageMetadata } from "@/types/concert";
import { getPagePngUrl } from "@/lib/api";
import { trackPageNavigation } from "@/lib/analytics";

interface ImageViewerProps {
  concertId: number;
  pages: PageMetadata[];
  currentPage: number;
  onPageChange: (page: number) => void;
}

export default function ImageViewer({
  concertId,
  pages,
  currentPage,
  onPageChange,
}: ImageViewerProps) {
  const [touchStart, setTouchStart] = useState(0);
  const [touchEnd, setTouchEnd] = useState(0);

  const goToPrevious = () => {
    if (currentPage > 1) {
      onPageChange(currentPage - 1);
      trackPageNavigation(concertId, currentPage - 1, "button");
    }
  };

  const goToNext = () => {
    if (currentPage < pages.length) {
      onPageChange(currentPage + 1);
      trackPageNavigation(concertId, currentPage + 1, "button");
    }
  };

  // Navigation clavier
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
        if (e.key === "ArrowLeft") {
            if (currentPage > 1) {
            onPageChange(currentPage - 1);
            trackPageNavigation(concertId, currentPage - 1, "keyboard");
            }
        } else if (e.key === "ArrowRight") {
            if (currentPage < pages.length) {
            onPageChange(currentPage + 1);
            trackPageNavigation(concertId, currentPage + 1, "keyboard");
            }
        }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [currentPage, pages.length]);

  // Swipe mobile
  const handleTouchStart = (e: React.TouchEvent) => {
    setTouchStart(e.targetTouches[0].clientX);
  };

  const handleTouchMove = (e: React.TouchEvent) => {
    setTouchEnd(e.targetTouches[0].clientX);
  };

  const handleTouchEnd = () => {
        if (touchStart - touchEnd > 75) {
            // Swipe left → next
            if (currentPage < pages.length) {
            onPageChange(currentPage + 1);
            trackPageNavigation(concertId, currentPage + 1, "swipe");
            }
        }

        if (touchStart - touchEnd < -75) {
            // Swipe right → previous
            if (currentPage > 1) {
            onPageChange(currentPage - 1);
            trackPageNavigation(concertId, currentPage - 1, "swipe");
            }
        }
    };

  const currentPageData = pages.find((p) => p.page_number === currentPage);

  return (
    <section className="relative">
      {/* Image principale */}
      <div
        className="relative bg-white rounded-lg shadow-lg overflow-hidden group"
        onTouchStart={handleTouchStart}
        onTouchMove={handleTouchMove}
        onTouchEnd={handleTouchEnd}
      >
        <div className="relative w-full aspect-[3/4] md:aspect-[4/3]">
          <img
            src={getPagePngUrl(concertId, currentPage)}
            alt={`Page ${currentPage}`}
            className="w-full h-full object-contain"
          />
        </div>

        {/* Boutons navigation - Hover uniquement */}
        {currentPage > 1 && (
          <button
            onClick={goToPrevious}
            className="absolute left-4 top-1/2 -translate-y-1/2 p-3 bg-black/50 hover:bg-black/70 text-white rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-200"
            aria-label="Page précédente"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M15 19l-7-7 7-7"
              />
            </svg>
          </button>
        )}

        {currentPage < pages.length && (
          <button
            onClick={goToNext}
            className="absolute right-4 top-1/2 -translate-y-1/2 p-3 bg-black/50 hover:bg-black/70 text-white rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-200"
            aria-label="Page suivante"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-6 w-6"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 5l7 7-7 7"
              />
            </svg>
          </button>
        )}
      </div>

      {/* Instructions clavier (desktop uniquement) */}
      <div className="hidden md:flex justify-center mt-4 text-sm text-gray-500">
        <span>
          Utilisez les flèches ← → pour naviguer
        </span>
      </div>
    </section>
  );
}