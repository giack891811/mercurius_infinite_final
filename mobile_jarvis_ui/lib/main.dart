import 'dart:async';
import 'package:flutter/material.dart';
import 'package:speech_to_text/speech_to_text.dart' as stt;
import 'package:flutter_tts/flutter_tts.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() => runApp(const JarvisApp());

class JarvisApp extends StatelessWidget {
  const JarvisApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Aion HUD',
      theme: ThemeData.dark(),
      home: const JarvisHomePage(),
    );
  }
}

class JarvisHomePage extends StatefulWidget {
  const JarvisHomePage({super.key});

  @override
  State<JarvisHomePage> createState() => _JarvisHomePageState();
}

class _JarvisHomePageState extends State<JarvisHomePage> {
  final stt.SpeechToText _speech = stt.SpeechToText();
  final FlutterTts _tts = FlutterTts();
  bool _isListening = false;
  String _lastWords = '';
  String _response = '';

  Future<void> _listen() async {
    if (!_isListening) {
      bool available = await _speech.initialize();
      if (available) {
        setState(() => _isListening = true);
        _speech.listen(onResult: (val) {
          setState(() => _lastWords = val.recognizedWords);
          if (val.hasConfidenceRating && val.confidence > 0) {
            _askBackend(_lastWords);
          }
        });
      }
    } else {
      setState(() => _isListening = false);
      _speech.stop();
    }
  }

  Future<void> _askBackend(String prompt) async {
    try {
      final resp = await http.post(
        Uri.parse('http://localhost:8000/ask'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'prompt': prompt}),
      ).timeout(const Duration(seconds: 5));
      if (resp.statusCode == 200) {
        final data = jsonDecode(resp.body);
        _response = data['response'] ?? '';
        _speak(_response);
        setState(() {});
      }
    } catch (_) {
      _speak('Attenda un istante, sto raccogliendo i dati Signore...');
    }
  }

  Future<void> _speak(String text) async {
    await _tts.setLanguage('it-IT');
    await _tts.speak(text);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: Center(
        child: GestureDetector(
          onTap: _listen,
          child: AnimatedContainer(
            duration: const Duration(milliseconds: 300),
            width: _isListening ? 200 : 150,
            height: _isListening ? 200 : 150,
            decoration: BoxDecoration(
              color: Colors.tealAccent.withOpacity(0.2),
              shape: BoxShape.circle,
              border: Border.all(color: Colors.tealAccent),
            ),
            child: Center(
              child: Text(
                _isListening ? 'Ascolto...' : 'Aion',
                style: const TextStyle(color: Colors.tealAccent, fontSize: 24),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
