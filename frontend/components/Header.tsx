import { Concert } from "@/types/concert";
import { getPdfUrl } from "@/lib/api";
import { trackPdfDownload } from "@/lib/analytics";

interface HeaderProps {
  concert: Concert;
  currentPage: number;
  totalPages: number;
}

export default function Header({ concert, currentPage, totalPages }: HeaderProps) {
  const formatDate = (dateString: string | null) => {
    if (!dateString) return null;
    const date = new Date(dateString);
    return date.toLocaleDateString("fr-FR", {
      day: "numeric",
      month: "long",
      year: "numeric",
    });
  };

  return (
    <>
      <header className="bg-white shadow-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 md:py-6">
          {/* Desktop */}
          <div className="hidden md:flex items-center justify-between">
            <div className="flex-1">
              <h1 className="text-2xl font-bold text-gray-900">{concert.title}</h1>
              <div className="flex gap-4 mt-2 text-sm text-gray-600">
                {concert.concert_date && <span>{formatDate(concert.concert_date)}</span>}
                {concert.location && <span>{concert.location}</span>}
              </div>
            </div>
            
            <div className="flex items-center gap-6">
              <span className="text-sm text-gray-600">
                Page {currentPage} / {totalPages}
              </span>
              <a
                href={getPdfUrl(concert.id)}
                target="_blank"
                rel="noopener noreferrer"
                onClick={() => trackPdfDownload(concert.id, concert.title)}
                className="px-4 py-2 bg-gray-900 text-white rounded-lg hover:bg-gray-700 transition-colors text-sm font-medium"
              >
                Télécharger PDF
              </a>
            </div>
          </div>

          {/* Mobile - Minimaliste */}
          <div className="md:hidden">
            <div className="flex items-center justify-between">
              <h1 className="text-lg font-bold text-gray-900 truncate flex-1">
                {concert.title}
              </h1>
              <span className="text-xs text-gray-600 ml-2">
                {currentPage}/{totalPages}
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Bouton PDF floating mobile - HORS du header */}
      <a
        href={getPdfUrl(concert.id)}
        target="_blank"
        rel="noopener noreferrer"
        onClick={() => trackPdfDownload(concert.id, concert.title)}
        className="md:hidden fixed bottom-4 right-4 p-3 bg-gray-900 text-white rounded-full shadow-lg hover:bg-gray-700 transition-colors z-50"
        aria-label="Télécharger PDF"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          className="h-5 w-5"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3V10"
          />
        </svg>
      </a>
    </>
  );
}