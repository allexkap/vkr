## Основные вопросы, подлежащие разработке / Key issues to be analyzed

### Техническое задание:
Разработать программное решение контейнеризации, обеспечивающее безопасное
выполнение недоверенного кода без использования привилегированных операций.
Решение должно быть легковесным, простым в эксплуатации и минимизировать риски
эскалации привилегий.

### Исходные данные к работе:
1. Анализ существующих решений: FireJail, Docker, LXC, Bubblewrap (код,
документация, статьи).
1. Изучение технологий виртуализации: Linux namespaces, seccomp, cgroups.
1. Исследования по безопасности контейнеров.

### Содержание работы:
1. Обзор существующих решений и их ограничений.
1. Обзор механизмов контейнеризации.
1. Проектирование архитектуры.
1. Разработка программного решения.
1. Демонстрация разработанного программного решения.
1. Тестирование безопасности изоляции процессов.
7. Подготовка разработанного решения к распространению.

### Цель работы:
Повышение пользовательской безопасности за счет создания инструмента запуска
недоверенного кода в изолированной среде без необходимости в использовании
привилегированных операций.

### Задачи работы:
1. Проанализировать существующие инструменты контейнеризации и их ограничения.
1. Определить ключевые требования к программному решению с учетом безопасности и
   удобства использования.
1. Разработать программное решение и провести его тестирование.
1. Провести сравнение разработанного решения с существующими аналогами.

### Перечень подлежащих разработке вопросов:
1. Выбор технологий изоляции.
1. Определение сценариев использования.
1. Выбор способа доставки программного решения.

### Рекомендуемые материалы для выполнения работы:
Официальная документация по технологиям контейнеризации и изоляции:
1. The Linux Kernel documentation // The Linux Kernel URL:
https://www.kernel.org/doc/html/latest/ (дата обращения: 21.03.25).
1. namespaces(7) — Linux manual page // Linux man pages online URL:
https://man7.org/linux/man-pages/man7/namespaces.7.html (дата обращения:
21.03.25).
1. SECure COMPuting with filters // The Linux Kernel URL:
https://www.kernel.org/doc/Documentation/prctl/seccomp_filter.txt (дата
обращения: 21.03.25).
1. Control Group v2 // The Linux Kernel URL:
https://www.kernel.org/doc/Documentation/cgroup-v2.txt (дата обращения:
21.03.25).

Документация и код существующих решений:
1. Security // Docker Docs URL: https://docs.docker.com/security/ (дата
обращения: 21.03.25).
1. What's LXC? // LXC URL: https://linuxcontainers.org/lxc/introduction/ (дата
обращения: 21.03.25).
1. bubblewrap // GitHub URL: https://github.com/containers/bubblewrap (дата
обращения: 21.03.25).
1. firejail // GitHub URL: https://github.com/netblue30/firejail (дата
обращения: 21.03.25).

Исследования в области безопасности контейнеров:
1. Understanding and Hardening Linux Containers // nccgroup URL:
https://www.nccgroup.com/media/eoxggcfy/_ncc_group_understanding_hardening_linux_containers-1-1.pdf
(дата обращения: 21.03.25).
1. Docker Security Cheat Sheet // OWASP Cheat Sheet Series URL:
https://cheatsheetseries.owasp.org/cheatsheets/Docker_Security_Cheat_Sheet.html
(дата обращения: 21.03.25).
