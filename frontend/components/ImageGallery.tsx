import { PageMetadata } from "@/types/concert";
import { getPagePngUrl } from "@/lib/api";

interface ImageGalleryProps {
  concertId: number;
  pages: PageMetadata[];
  currentPage: number;
  onPageSelect: (page: number) => void;
}

export default function ImageGallery({
  concertId,
  pages,
  currentPage,
  onPageSelect,
}: ImageGalleryProps) {
  return (
    <section className="mt-8">
      <h2 className="text-xl font-semibold text-gray-900 mb-4">
        Toutes les pages
      </h2>
      
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
        {pages.map((page) => (
          <button
            key={page.id}
            onClick={() => onPageSelect(page.page_number)}
            className={`
              relative aspect-[3/4] rounded-lg overflow-hidden
              transition-all duration-200
              ${
                currentPage === page.page_number
                  ? "ring-4 ring-gray-900 shadow-xl scale-105"
                  : "ring-1 ring-gray-200 hover:ring-2 hover:ring-gray-400 hover:shadow-lg"
              }
            `}
          >
            <img
              src={getPagePngUrl(concertId, page.page_number)}
              alt={`Page ${page.page_number}`}
              className="w-full h-full object-cover"
            />
            
            {/* Numéro de page */}
            <div className="absolute bottom-2 right-2 bg-black/70 text-white text-xs font-medium px-2 py-1 rounded">
              {page.page_number}
            </div>
            
            {/* Overlay hover */}
            <div className="absolute inset-0 bg-black/0 hover:bg-black/10 transition-colors" />
          </button>
        ))}
      </div>
    </section>
  );
}