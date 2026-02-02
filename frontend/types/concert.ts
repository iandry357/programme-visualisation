export interface Concert {
  id: number;
  title: string;
  concert_date: string | null;
  location: string | null;
  is_published: boolean;
  pdf_filename: string;
  pdf_size: number;
  created_at: string | null;
  updated_at: string | null;
  pages: PageMetadata[];
}

export interface PageMetadata {
  id: number;
  page_number: number;
  width: number | null;
  height: number | null;
  png_size: number;
}