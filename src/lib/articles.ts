import { getCollection, type CollectionEntry } from 'astro:content';
import { BIKE_TYPE_SLUGS, MACRO_CATEGORY_SLUGS } from '../content.config';

export type Article = CollectionEntry<'articles'>;
export type CategorySlug = Article['data']['categories'][number];
export type Locale = 'it' | 'en' | 'es';

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

export async function getArticlesByCategory(category: CategorySlug): Promise<Article[]> {
  const all = await getPublishedArticles();
  return all.filter((article) => article.data.categories.includes(category));
}

// Etichette tradotte IT/EN/ES, in sync a mano con il Google Sheet
// "Bike-Style-Mag_Elenco-Categorie" in 00_GUIDE BIKE STYLE su Drive. Il sito è oggi
// solo in inglese: `categoryLabel()` usa "en" di default finché non esiste un routing
// multi-lingua, ma le traduzioni sono già pronte per quando servirà.
const CATEGORY_LABELS: Record<CategorySlug, Record<Locale, string>> = {
  'urban-bike': { it: 'Bici urbana', en: 'Urban bike', es: 'Bici urbana' },
  'road-bike': { it: 'Bici da corsa', en: 'Road bike', es: 'Bici de carretera' },
  'mountain-bike': { it: 'Mountain bike', en: 'Mountain bike', es: 'Bicicleta de montaña' },
  gravel: { it: 'Gravel', en: 'Gravel', es: 'Gravel' },
  'cargo-bike': { it: 'Cargo bike', en: 'Cargo bike', es: 'Bici de carga' },
  folding: { it: 'Pieghevole', en: 'Folding', es: 'Plegable' },
  bmx: { it: 'BMX', en: 'BMX', es: 'BMX' },
  'fixed-gear': { it: 'Scatto fisso', en: 'Fixed-gear', es: 'Piñón fijo' },
  luxury: { it: 'Lusso', en: 'Luxury', es: 'Lujo' },
  design: { it: 'Design', en: 'Design', es: 'Diseño' },
  culture: { it: 'Cultura', en: 'Culture', es: 'Cultura' },
  bicycle: { it: 'Bicicletta', en: 'Bicycle', es: 'Bicicleta' },
  'e-bike': { it: 'E-bike', en: 'E-bike', es: 'Bicicleta eléctrica' },
  clothing: { it: 'Abbigliamento', en: 'Apparel', es: 'Ropa' },
  accessories: { it: 'Accessori', en: 'Accessories', es: 'Accesorios' },
  infrastructure: { it: 'Infrastrutture', en: 'Infrastructure', es: 'Infraestructura' },
  travel: { it: 'Viaggi', en: 'Travel', es: 'Viajes' },
  spots: { it: 'Indirizzi', en: 'Spots', es: 'Lugares' },
  'events-awards': { it: 'Eventi e premi', en: 'Events & awards', es: 'Eventos y premios' },
  technology: { it: 'Tecnologia', en: 'Technology', es: 'Tecnología' },
  reviews: { it: 'Recensioni', en: 'Reviews', es: 'Reseñas' },
};

export function categoryLabel(category: CategorySlug, locale: Locale = 'en'): string {
  return CATEGORY_LABELS[category][locale];
}

const BIKE_TYPE_SET = new Set<string>(BIKE_TYPE_SLUGS);
const MACRO_CATEGORY_SET = new Set<string>(MACRO_CATEGORY_SLUGS);

export type CategoryGroup = 'bikeType' | 'macro';

export function categoryGroup(category: CategorySlug): CategoryGroup {
  if (BIKE_TYPE_SET.has(category)) return 'bikeType';
  if (MACRO_CATEGORY_SET.has(category)) return 'macro';
  throw new Error(`Unknown category slug: ${category}`);
}
