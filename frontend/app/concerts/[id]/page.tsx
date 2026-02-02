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

  useEffect(() => {
    async function fetchConcert() {
      try {
        setLoading(true);
        const data = await getConcert(concertId);
        setConcert(data);
        setError(null);
      } catch (err) {
        setError("Impossible de charger le concert");
        console.error(err);
      } finally {
        setLoading(false);
      }
    }

    fetchConcert();
  }, [concertId]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mx-auto mb-4"></div>
          <p className="text-gray-600">Chargement...</p>
        </div>
      </div>
    );
  }

  if (error || !concert) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <p className="text-red-600 text-lg">{error || "Concert introuvable"}</p>
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