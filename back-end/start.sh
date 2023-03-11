#!/usr/bin/env bash

until cd /app && composer install && composer require laravel/octane spiral/roadrunner && npm install
do
    echo "Retrying"
done
php artisan key:generate
npm run dev
php artisan serve
