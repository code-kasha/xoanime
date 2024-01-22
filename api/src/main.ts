require('dotenv').config();

import Fastify from 'fastify';
import FastifyCors from '@fastify/cors';

import anime from './routes/anime';
import manga from './routes/manga';
import lightnovels from './routes/light-novels';
import news from './routes/news';

import chalk from 'chalk';

(async () => {
  const PORT = Number(process.env.PORT) || 3000;

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
  await fastify.register(lightnovels, { prefix: '/light-novels' });
  await fastify.register(news, { prefix: '/news' });

  try {
    fastify.get('/', (_, rp) => {
      rp.status(200).send(`Welcome to XO Anime api! 🎉 `);
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
