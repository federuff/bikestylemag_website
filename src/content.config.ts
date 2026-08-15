import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

// Elenco canonico (slug tecnico, sempre in inglese) mantenuto in sync a mano con il
// Google Sheet "Bike-Style-Mag_Elenco-Categorie" in 00_GUIDE BIKE STYLE su Drive, dove
// vivono anche le etichette tradotte IT/EN/ES e le descrizioni per la redazione.
export const BIKE_TYPE_SLUGS = [
  'urban-bike',
  'road-bike',
  'mountain-bike',
  'gravel',
  'cargo-bike',
  'folding',
  'bmx',
  'fixed-gear',
] as const;

export const MACRO_CATEGORY_SLUGS = [
  'luxury',
  'design',
  'culture',
  'bicycle',
  'e-bike',
  'clothing',
  'accessories',
  'infrastructure',
  'travel',
  'spots',
  'events-awards',
  'technology',
  'reviews',
] as const;

export const CATEGORY_SLUGS = [...BIKE_TYPE_SLUGS, ...MACRO_CATEGORY_SLUGS] as const;

const articles = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/articles' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    // Un articolo può avere più categorie insieme (es. ["accessories", "urban-bike"],
    // o ["e-bike", "road-bike"] per una bici da corsa a pedalata assistita).
    categories: z.array(z.enum(CATEGORY_SLUGS)).min(1),
    heroImage: z.string().optional(),
    sourceUrl: z.url().optional(),
    sourceName: z.string().optional(),
    author: z.string().default('BikeStyle Mag Editorial Team'),
    draft: z.boolean().default(true),
  }),
});

export const collections = { articles };
