import rss from '@astrojs/rss';
import { getPublishedArticles } from '../lib/articles';

export async function GET(context) {
  const articles = await getPublishedArticles();

  return rss({
    title: 'BikeStyle Mag',
    description: 'Design, bicycles and sustainable urban mobility.',
    site: context.site,
    items: articles.map((article) => ({
      title: article.data.title,
      description: article.data.description,
      pubDate: article.data.pubDate,
      link: `/articles/${article.id}`,
    })),
  });
}
