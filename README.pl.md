# ASCII Video Generator

ASCII Video Generator to aplikacja w Pythonie, która konwertuje plik wideo/animacji do filmu w formie ASCII art. Aplikacja wykorzystuje OpenCV do ekstrakcji klatek wideo, przetwarza każdą klatkę, aby wygenerować ASCII art, a następnie łączy te klatki w nowy film za pomocą MoviePy. Graficzny interfejs użytkownika (GUI) został zbudowany przy użyciu Tkinter, co pozwala użytkownikom dostosować różne ustawienia i podglądać konwersję w czasie rzeczywistym.

![image](https://github.com/user-attachments/assets/67900d53-e4e2-482d-b611-156e3ad97ff0)

## Funkcje

- **Konwersja wideo na ASCII:**  
  Konwertuj każdą klatkę wideo na ASCII art z możliwością dostosowania parametrów.

- **Możliwość dostosowania ustawień:**  
  Dostosuj wymiary wyjściowe, rozmiar czcionki, gamma, jasność, kontrast oraz kolor tekstu w formacie RGB przy użyciu intuicyjnych suwaków.

- **Wsparcie dla niestandardowych czcionek:**  
  Załaduj niestandardowy plik czcionki do renderowania ASCII art.

- **Podgląd w czasie rzeczywistym:**  
  Podgląd pierwszej przekonwertowanej klatki przed przetworzeniem całego wideo.

- **Generowanie filmu wyjściowego:**  
  Łączy przetworzone klatki w ostateczny film z ASCII art.

- **Logowanie i obsługa błędów:**  
  Aplikacja zapisuje kroki przetwarzania oraz błędy w pliku `ascii_art_generator.log`, co ułatwia debugowanie.

## Instalacja

1. **Sklonuj repozytorium:**
    ```bash
    git clone https://github.com/Gulwe/ASCII-Video-Generator
    cd ascii-video-generator
    ```

2. **Zainstaluj wymagane zależności:**
    ```bash
    pip install opencv-python numpy Pillow moviepy
    ```

3. **Uruchom aplikację:**
    ```bash
    python ascii_video_generator.py
    ```

## Użytkowanie

1. **Wybierz plik wideo:**  
   Kliknij przycisk "Select Video File", aby wybrać wideo, które chcesz przekonwertować.

2. **Załaduj niestandardową czcionkę (opcjonalnie):**  
   Użyj przycisku "Load Custom Font", aby załadować preferowaną czcionkę TTF lub OTF.

3. **Dostosuj ustawienia:**  
   - **Wymiary wyjściowe:** Użyj suwaka "Output Size", aby ustawić szerokość wyjściowego ASCII.
   - **Rozmiar czcionki:** Dostosuj rozmiar czcionki dla renderowania ASCII.
   - **Gamma, jasność, kontrast:** Dostosuj wizualny wygląd ASCII art.
   - **Kolory RGB:** Ustaw kolor tekstu dla znaków ASCII.
   - **Pominięcie klatek & FPS:** Kontroluj prędkość konwersji oraz liczbę klatek na sekundę w filmie wyjściowym.

4. **Podgląd:**  
   W sekcji "Preview" wyświetlany jest podgląd pierwszej przekonwertowanej klatki.

5. **Konwertuj:**  
   Kliknij przycisk "Convert", aby rozpocząć przetwarzanie wideo. Ostateczny film z ASCII art zostanie zapisany w tym samym katalogu co plik źródłowy, z dopiskiem `_ASCII.mp4` do nazwy pliku.

## Struktura kodu

- **Główne moduły:**  
  - `frame_to_ascii_text()`: Konwertuje klatki wideo na tekst ASCII.
  - `ascii_text_to_image()`: Renderuje tekst ASCII do obrazu.
  - `frame_generator_sequential()`: Generator przetwarzający klatki wideo sekwencyjnie.
  - Klasa `App`: Obsługuje interfejs Tkinter, interakcje z użytkownikiem oraz ogólny przepływ przetwarzania wideo.

- **Logowanie:**  
  Wszystkie kroki przetwarzania oraz błędy są zapisywane w pliku `ascii_art_generator.log`.

## Roadmap / Dalszy rozwój

- **Lepsza optymalizacja:** Poprawa wydajności przetwarzania wideo oraz zarządzania pamięcią.
- **Możliwość zapisywania do GIF:** Rozszerzenie funkcjonalności o eksport do formatu GIF.

## Wkład / Contributing

Wkład w projekt jest mile widziany! Zachęcamy do zgłaszania problemów oraz przesyłania pull requestów z ulepszeniami i nowymi funkcjami.

![cat-space gif_ASCII](https://github.com/user-attachments/assets/dec78fd3-2d23-4300-b714-ab8fb4982524)
