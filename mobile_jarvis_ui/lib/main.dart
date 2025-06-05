import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:speech_to_text/speech_to_text.dart' as stt;
import 'package:flutter_tts/flutter_tts.dart';
import 'package:http/http.dart' as http;

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
  String? _selectedBackendIP; // L'IP attualmente selezionato
  final List<String> _hotwords = ['hey mercurius', 'aion attivati'];
  final _foundDevices = <String>[];


  // Utility per prendere l'IP del gateway (funziona per la maggior parte delle reti)
  Future<String?> _getGatewayIp() async {
    try {
      for (var interface in await NetworkInterface.list()) {
        for (var addr in interface.addresses) {
          if (addr.type == InternetAddressType.IPv4 && !addr.address.startsWith('127.')) {
            var ip = addr.address.split('.');
            return '${ip[0]}.${ip[1]}.${ip[2]}.1';
          }
        }
      }
    } catch (_) {}
    return null;
  }

  // Scansiona la rete locale per trovare altri dispositivi (ping a /24)
  Future<void> _scanDevices() async {
    setState(() {
      _foundDevices.clear();
    });

    final gateway = await _getGatewayIp();
    if (gateway == null) return;

    final subnet = gateway.substring(0, gateway.lastIndexOf('.') + 1);
    List<Future> futures = [];

    for (int i = 1; i < 255; i++) {
      final ip = '$subnet$i';
      futures.add(_ping(ip));
    }

    await Future.wait(futures);
    setState(() {});
  }

  // Pinga un singolo IP per vedere se è attivo
  Future<void> _ping(String ip) async {
    try {
      final result = await Socket.connect(ip, 8000, timeout: const Duration(milliseconds: 300));
      result.destroy();
      if (!_foundDevices.contains(ip)) {
        setState(() {
          _foundDevices.add(ip);
        });
      }
    } catch (_) {}
  }

  // Usa l'IP selezionato (o il primo trovato) come backend
  String get _backendUrl {
    if (_selectedBackendIP != null) {
      return 'http://${_selectedBackendIP!}:8000/ask';
    }
    // Default fallback (localhost per debug su PC, va cambiato su mobile)
    return 'http://172.18.208.1:8000/ask';
  }

  Future<void> _listen() async {
    if (!_isListening) {
      bool available = await _speech.initialize();
      if (available) {
        setState(() => _isListening = true);
        _speech.listen(onResult: (val) {
          setState(() => _lastWords = val.recognizedWords);
          final words = val.recognizedWords.toLowerCase();
          if (_hotwords.any((hw) => words.contains(hw))) {
            _speech.stop();
            setState(() => _isListening = false);
            _speak('Pronto, Signore.');
          } else if (val.hasConfidenceRating && val.confidence > 0) {
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
        Uri.parse(_backendUrl),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'prompt': prompt}),
      ).timeout(const Duration(seconds: 5));
      if (resp.statusCode == 200) {
        final data = jsonDecode(resp.body);
        _response = data['response'] ?? '';
        _speak(_response);
        setState(() {});
      }
    } catch (e) {
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
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            GestureDetector(
              onTap: _listen,
              child: AnimatedContainer(
                duration: const Duration(milliseconds: 300),
                width: _isListening ? 200 : 150,
                height: _isListening ? 200 : 150,
                decoration: BoxDecoration(
                  color: Colors.tealAccent.withAlpha((0.2 * 255).round()),
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
            const SizedBox(height: 20),

            // SELEZIONE BACKEND
            ElevatedButton.icon(
              icon: const Icon(Icons.search),
              label: const Text("Scansiona Rete"),
              onPressed: _scanDevices,
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.teal,
              ),
            ),
            if (_foundDevices.isNotEmpty)
              Wrap(
                children: _foundDevices
                    .map((ip) => Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 4.0),
                  child: ChoiceChip(
                    label: Text(ip, style: const TextStyle(color: Colors.white)),
                    selected: _selectedBackendIP == ip,
                    onSelected: (_) {
                      setState(() {
                        _selectedBackendIP = ip;
                      });
                    },
                    selectedColor: Colors.tealAccent,
                  ),
                ))
                    .toList(),
              ),
            const SizedBox(height: 10),
            Text(
              _response,
              textAlign: TextAlign.center,
              style: const TextStyle(color: Colors.tealAccent),
            ),
          ],
        ),
      ),
    );
  }
}
