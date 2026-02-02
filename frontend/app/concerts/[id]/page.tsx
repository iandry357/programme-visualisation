"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { getConcert } from "@/lib/api";
import { Concert } from "@/types/concert";
import Header from "@/components/Header";
import ImageGallery from "@/components/ImageGallery";
import ImageViewer from "@/components/ImageViewer";

export default function ConcertPage() {
  const params = useParams();
  const concertId = Number(params.id);

  const [concert, setConcert] = useState<Concert | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isRetrying, setIsRetrying] = useState(false);

  const fetchConcert = async (retryCount = 0) => {
    setError(null);
    setIsRetrying(retryCount > 0);
    setLoading(true);

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 20000); // 20s timeout

    try {
      const data = await getConcert(concertId, controller.signal);
      setConcert(data);
      setError(null);
    } catch (err: any) {
      if (err.name === 'AbortError') {
        setError('Le chargement prend trop de temps');
      } else if (err.message === 'Failed to fetch' || err.message?.includes('fetch')) {
        setError('Impossible de contacter le serveur');
      } else if (err.message?.includes('404') || err.message?.includes('not found')) {
        setError('Concert non trouvé');
      } else {
        setError('Une erreur est survenue lors du chargement');
      }
      console.error(err);
    } finally {
      clearTimeout(timeoutId);
      setLoading(false);
      setIsRetrying(false);
    }
  };

  useEffect(() => {
    fetchConcert();
  }, [concertId]);

  const handleRetry = () => {
    fetchConcert(1);
  };

  const handleImageError = () => {
    setError('Erreur lors du chargement de l\'image');
  };

  // Affichage erreur
  if (error && !loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black flex items-center justify-center px-4">
        <div className="text-center max-w-md">
          <div className="mb-6">
            <svg 
              className="w-16 h-16 mx-auto text-red-500" 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                strokeWidth={2} 
                d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
          </div>
          <h2 className="text-2xl font-semibold text-white mb-4">{error}</h2>
          <button
            onClick={handleRetry}
            disabled={isRetrying}
            className="bg-white text-black px-6 py-3 rounded-lg font-medium hover:bg-gray-200 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isRetrying ? 'Chargement...' : 'Réessayer'}
          </button>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto mb-4"></div>
          <p className="text-gray-300">Chargement...</p>
        </div>
      </div>
    );
  }

  if (!concert) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black flex items-center justify-center px-4">
        <div className="text-center">
          <p className="text-red-400 text-lg">Concert introuvable</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header
        concert={concert}
        currentPage={currentPage}
        totalPages={concert.pages.length}
      />
      
      <main className="container mx-auto px-4 py-8">
        <ImageViewer
          concertId={concert.id}
          pages={concert.pages}
          currentPage={currentPage}
          onPageChange={setCurrentPage}
          onImageError={handleImageError}
        />
        
        {/* <ImageGallery
          concertId={concert.id}
          pages={concert.pages}
          currentPage={currentPage}
          onPageSelect={setCurrentPage}
        /> */}
      </main>
    </div>
  );
}