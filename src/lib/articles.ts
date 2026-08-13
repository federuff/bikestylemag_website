import { getCollection, type CollectionEntry } from 'astro:content';

export type Article = CollectionEntry<'articles'>;

/**
 * Unico punto da cui leggere gli articoli per qualsiasi pagina/feed pubblico.
 * In build (produzione) esclude le bozze; in dev le mostra tutte, per permettere
 * la revisione umana di un articolo scritto da un agente prima della pubblicazione.
 */
export async function getPublishedArticles(): Promise<Article[]> {
  const all = await getCollection('articles', ({ data }) => {
    return import.meta.env.PROD ? data.draft === false : true;
  });
  return all.sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());
}

const CATEGORY_LABELS: Record<Article['data']['category'], string> = {
  luxury: 'Luxury',
  ebike: 'E-bike',
  design: 'Design',
  urban_commuter: 'Urban Commuter',
  general: 'General',
};

export function categoryLabel(category: Article['data']['category']): string {
  return CATEGORY_LABELS[category];
}
