import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const articles = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/articles' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    category: z.enum(['luxury', 'ebike', 'design', 'urban_commuter', 'general']),
    heroImage: z.string().optional(),
    sourceUrl: z.url().optional(),
    sourceName: z.string().optional(),
    author: z.string().default('BikeStyle Mag Editorial Team'),
    draft: z.boolean().default(true),
  }),
});

export const collections = { articles };
