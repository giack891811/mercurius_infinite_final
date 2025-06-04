# Mobile Jarvis UI

Flutter-based HUD interface for Mercurius∞. The app offers voice interaction using
`speech_to_text` and `flutter_tts`, with simple hotword detection ("Hey Mercurius"
or "Aion attivati"). Requests are sent to the local Aion API (`/ask`) which in
turn forwards them to the orchestrator.

Build and run using the Flutter SDK on an Android device:

```bash
flutter run -d android
```
