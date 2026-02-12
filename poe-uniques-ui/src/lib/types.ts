export type BaseItem = {
  id: number;
  name: string;
  item_class: string;
  slot: string;
}

export type UniqueItem = {
  id: number;
  name: string;
  required_level: number | null;
  image_url: string;
  base_item: BaseItem;
  flavour_text: string;

  chaos_value: string | null;
  divine_value: string | null;
  listing_count: number | null;
}

export type Paginated<T> = {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export type UniqueQuery = { 
  page?: string;
  search?: string;
  ordering?: string;
  league?: string;
}