require('dotenv').config();

import Fastify from 'fastify';
import FastifyCors from '@fastify/cors';

import anime from './routes/anime';
import manga from './routes/manga';
import novels from './routes/novels';
import news from './routes/news';

import chalk from 'chalk';

(async () => {
  const PORT = Number(process.env.PORT);

  const fastify = Fastify({
    maxParamLength: 1000,
    logger: true,
  });
  await fastify.register(FastifyCors, {
    origin: '*',
    methods: 'GET',
  });

  console.log(chalk.green(`Starting server on port ${PORT}... 🚀`));

  await fastify.register(anime, { prefix: '/anime' });
  await fastify.register(manga, { prefix: '/manga' });
  await fastify.register(novels, { prefix: '/novels' });
  await fastify.register(news, { prefix: '/news' });

  try {
    fastify.get('/', (_, rp) => {
      rp.status(200).send({
        intro: `Welcome to XO Anime - API.`,
        routes: [
          '/anime - Powered by Gogoanime @ https://anitaku.to',
          '/manga - Powered by Mangasee123 @ https://mangasee123.com',
          '/news - Powered by Anime News Network @ https://animenewsnetwork.com',
          '/novels - Powered by Read Light Novels @ https://animedaily.net/',
        ],
      });
    });
    fastify.get('*', (request, reply) => {
      reply.status(404).send({
        message: '',
        error: 'page not found',
      });
    });

    fastify.listen({ port: PORT, host: '0.0.0.0' }, (e, address) => {
      if (e) throw e;
      console.log(`server listening on ${address}`);
    });
  } catch (err: any) {
    fastify.log.error(err);
    process.exit(1);
  }
})();
