export type BaseItem = {
  id: number;
  name: string;
  item_class: string;
  slot: string;
  icon_url: string;
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

  ancient_meta?: {
    tier: number | null;
    chance: number | null;
    avg_orbs: number | null;
    min_ilvl: number | null;
    pool?: string | null;
    source?: string | null;
  }
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