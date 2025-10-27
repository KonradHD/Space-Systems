# Zadanie rekrutacyjne, AGH Space Systems Rocket Software jesień 2025

W ramach zadania rekrutacyjnego przygotowałem prostą grę/aplikację webową polegającą na ułożeniu klocków w odpowiedniej kolejności, aby rakieta bezpiecznie wystartowała oraz wylądowała. Dostępne są opcje podpowiedzi, aby zapoznać użytkownika z wymaganiami m.in. startu rakiety. Użytkownik na bieżąco może śledzić postęp w parametrach przedstawionych części rakiety, a o wszelkich błędach czy ekplozjach jest natychmiast informowany. W planach miałem zrobienie symulacji lotu rakiety, ale niestety zabrakło trochę czasu.

W zadaniu wykorzystałem framework Flask jako lekki serwer backendowy, który obsługuje żądania HTTP do komunikacji z frontendem. Do przesyłania danych w czasie rzeczywistym zastosowaem technologię Server-Sent Events (SSE), dzięki której serwer może szybko przesyłać dane. Mechanizm ten działa w oparciu o Redis, który pełni rolę pośrednika między serwerem a klientami SSE.  
