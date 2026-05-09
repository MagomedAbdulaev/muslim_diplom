from django.http import JsonResponse
from django.shortcuts import render
import os
import json
from ollama import Client


def home(request):
    context = {
        'title': 'Главная'
    }
    return render(request, 'home.html', context)


def get_suppliers(request):
    # 1. Получаем параметры
    experience = request.GET.get('experience', 'ЛЮБОЙ')
    # Проверяем на строку 'true', так как URLSearchParams отправляет типы как строки
    phone_only = request.GET.get('phone_only') == 'true'
    rating = request.GET.get('rating', 'ЛЮБОЙ')
    search = request.GET.get('search')
    city = request.GET.get('city', 'Махачкала')

    client = Client(
        host="https://ollama.com",
        headers={'Authorization': 'Bearer ' + ''}
    )

    prompt = (
        f"Роль: Ты — эксперт по анализу рынка строительных материалов. Бери информацию настоящую, из интернета, пожалуйста.\n"
        f"Задача: Подготовить JSON-массив (Как можно больше записей) поставщиков в г. {city}.\n"
        f"Условия: Специализация '{search}', стаж от {experience} лет, рейтинг от {rating}.\n"
        f"Связь: {'ТОЛЬКО С ТЕЛЕФОНОМ' if phone_only else 'ТЕЛЕФОН НЕ ОБЯЗАТЕЛЕН'}.\n"
        f"Формат: Только чистый JSON массив объектов с ключами: name, owner, phone, email, address, city, experience, rating, reviews, description, data_completeness, contacts_presence."
    )

    full_content = ""
    try:
        # 2. Собираем стрим в одну строку
        # Если модель поддерживает не-стримовый режим, лучше использовать stream=False для простоты
        for part in client.chat('gpt-oss:120b', messages=[{'role': 'user', 'content': prompt}], stream=True):
            full_content += part['message']['content']

        # 3. Очищаем ответ от Markdown-разметки (если нейросеть добавила ```json ... ```)
        clean_json = full_content.replace('```json', '').replace('```', '').strip()

        # 4. Преобразуем строку в Python-список, чтобы JsonResponse корректно его запаковал
        data_list = json.loads(clean_json)

        return JsonResponse({"data": data_list}, safe=False)

    except json.JSONDecodeError:
        # Если нейросеть выдала текст вместо JSON
        return JsonResponse({
            "error": "Ошибка парсинга JSON",
            "raw_response": full_content
        }, status=500)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
