#!/usr/bin/env bash

until cd /app && composer install && composer require laravel/octane spiral/roadrunner && npm install
do
    echo "Retrying"
done
php artisan key:generate
php artisan octane:install --server="swoole"
php artisan octane:start --server="swoole" --host="0.0.0.0"
npm run dev