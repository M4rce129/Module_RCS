#include <IRremote.hpp>

const int LED_B = 7;
const int LED_R = 8;
const int sensor = 11;
const int Audio = 3;
bool Activo = false;
bool MODE = false;

uint32_t codigoHEX;

void beep(int veces, int duracionMs)
{
  for (int i = 0; i < veces; i++)
  {
    digitalWrite(Audio, HIGH);
    delay(duracionMs);
    digitalWrite(Audio, LOW);
    delay(duracionMs);
  }
}

void LED_Active(int pin)
{
  digitalWrite(pin, HIGH);
  delay(150);
  digitalWrite(pin, LOW);

  if (pin == LED_B)
  {
    beep(1, 100);
  }
  else if (pin == LED_R)
  {
    beep(2, 70);
  }
}

void sendKey(const char *key)
{
  // Línea “limpia” para el listener de Linux
  Serial.print("KEY:");
  Serial.println(key);
}

void setup()
{
  // Activamos el receptor
  Activo = true;
  MODE = false;
  Serial.begin(9600);
  IrReceiver.begin(sensor, ENABLE_LED_FEEDBACK);
  // Configuramos salidas
  pinMode(LED_B, OUTPUT);
  pinMode(LED_R, OUTPUT);
  pinMode(Audio, OUTPUT);
  // CHECK
  LED_Active(LED_B);
  LED_Active(LED_R);
}

void loop()
{

  if (IrReceiver.decode())
  {

    codigoHEX = IrReceiver.decodedIRData.decodedRawData;

    // Debug opcional (Linux lo ignorará si empieza con DEBUG:)
    Serial.print("DEBUG:0x");
    Serial.println(codigoHEX, HEX);
    // Controlar el ingreso de comandos de forma remota
    if (codigoHEX == 0xBA45FF00)
    { // Registramos el boton de ONOFF sin inportar si esta activo o no
      // Invertimos el estado del Encendido
      Activo = !Activo;
      sendKey("ONOFF");
      LED_Active(LED_R);
      IrReceiver.resume();
      // Encedido -- LED apagado
      if (Activo == true)
      {
        Serial.println("Encendido");
        digitalWrite(LED_R, LOW);
      }
      // Apagado -- LED encendido
      if (Activo == false)
      {
        Serial.println("Apagado");
        digitalWrite(LED_R, HIGH);
      }
      // LED = ¡Activo
      return;
    }
    // Controlar el ingreso de comandos de forma remota para el modo MODE
    if (codigoHEX == 0xB946FF00)
    { // Activar modo MODE
      MODE = !MODE;
      sendKey("MODE");
      LED_Active(LED_R);
      IrReceiver.resume();
      if (MODE == true)
      {
        Serial.println("Modo MODE Activado");
        digitalWrite(LED_B, HIGH);
      }
      if (MODE == false)
      {
        Serial.println("Modo MODE Desactivado");
        digitalWrite(LED_B, LOW);
      }
      return;
    }

    if (Activo == true)
    {
      if (MODE == false) // Seccion Base de comandos
      {
        switch (codigoHEX)
        {

          // ----- BOTONES NUMÉRICOS => LED AZUL -----

        case 0xE916FF00:     // Detectamos el INPUT
          sendKey("0");      // Comando que envia el mensaje al .py
          LED_Active(LED_B); // Activacion del led correspondiente
          break;

        case 0xF30CFF00:
          sendKey("1");
          LED_Active(LED_B);
          break; // linea sintetizada
        case 0xE718FF00:
          sendKey("2");
          LED_Active(LED_B);
          break;
        case 0xA15EFF00:
          sendKey("3");
          LED_Active(LED_B);
          break;
        case 0xF708FF00:
          sendKey("4");
          LED_Active(LED_B);
          break;
        case 0xE31CFF00:
          sendKey("5");
          LED_Active(LED_B);
          break;
        case 0xA55AFF00:
          sendKey("6");
          LED_Active(LED_B);
          break;
        case 0xBD42FF00:
          sendKey("7");
          LED_Active(LED_B);
          break;
        case 0xAD52FF00:
          sendKey("8");
          LED_Active(LED_B);
          break;
        case 0xB54AFF00:
          sendKey("9");
          LED_Active(LED_B);
          break;

        // ----- OTROS BOTONES => LED ROJO -----
        case 0xB946FF00:
          sendKey("MODE");
          LED_Active(LED_R);
          break;
        case 0xB847FF00:
          sendKey("VolOFF");
          LED_Active(LED_R);
          break;
        case 0xBB44FF00:
          sendKey("Pausa");
          LED_Active(LED_R);
          break;
        case 0xBC43FF00:
          sendKey("Left");
          LED_Active(LED_R);
          break;
        case 0xBF40FF00:
          sendKey("Rigt");
          LED_Active(LED_R);
          break;
        case 0xF807FF00:
          sendKey("EQ");
          LED_Active(LED_R);
          break;
        case 0xEA15FF00:
          sendKey("-");
          LED_Active(LED_R);
          break;
        case 0xF609FF00:
          sendKey("+");
          LED_Active(LED_R);
          break;
        case 0xBA45FF00:
          sendKey("ONOFF");
          LED_Active(LED_R);
          break;
        case 0xE619FF00:
          sendKey("Cambio");
          LED_Active(LED_R);
          break;
        case 0xF20DFF00:
          sendKey("USB");
          LED_Active(LED_R);
          break;
        // ----- INPUTs desconocidos -----
        default:
          sendKey("UNMAPPED");
          LED_Active(LED_R);
          break;
        }
      }
      if (MODE == true) // Seccion de comandos para el modo MODE
      {
        switch (codigoHEX)
        {

          // ----- BOTONES NUMÉRICOS + MODE => LED ROJO -----

        case 0xE916FF00:     // Detectamos el INPUT
          sendKey("MODE0");  // Comando que envia el mensaje al .py
          LED_Active(LED_R); // Activacion del led correspondiente
          break;

        case 0xF30CFF00:
          sendKey("MODE1");
          LED_Active(LED_R);
          break; // linea sintetizada
        case 0xE718FF00:
          sendKey("MODE2");
          LED_Active(LED_R);
          break;
        case 0xA15EFF00:
          sendKey("MODE3");
          LED_Active(LED_R);
          break;
        case 0xF708FF00:
          sendKey("MODE4");
          LED_Active(LED_R);
          break;
        case 0xE31CFF00:
          sendKey("MODE5");
          LED_Active(LED_R);
          break;
        case 0xA55AFF00:
          sendKey("MODE6");
          LED_Active(LED_R);
          break;
        case 0xBD42FF00:
          sendKey("MODE7");
          LED_Active(LED_R);
          break;
        case 0xAD52FF00:
          sendKey("MODE8");
          LED_Active(LED_R);
          break;
        case 0xB54AFF00:
          sendKey("MODE9");
          LED_Active(LED_R);
          break;

        // ----- OTROS BOTONES => LED ROJO -----
        case 0xB946FF00:
          sendKey("MODE");
          LED_Active(LED_R);
          break;
        case 0xB847FF00:
          sendKey("VolOFF");
          LED_Active(LED_R);
          break;
        case 0xBB44FF00:
          sendKey("MODEPausa");
          LED_Active(LED_R);
          break;
        case 0xBC43FF00:
          sendKey("MODELeft");
          LED_Active(LED_R);
          break;
        case 0xBF40FF00:
          sendKey("MODERigt");
          LED_Active(LED_R);
          break;
        case 0xF807FF00:
          sendKey("MODE");
          LED_Active(LED_R);
          break;
        case 0xEA15FF00:
          sendKey("MODE-");
          LED_Active(LED_R);
          break;
        case 0xF609FF00:
          sendKey("MODE+");
          LED_Active(LED_R);
          break;
        case 0xBA45FF00:
          sendKey("ONOFF");
          LED_Active(LED_R);
          break;
        case 0xE619FF00:
          sendKey("Cambio");
          LED_Active(LED_R);
          break;
        case 0xF20DFF00:
          sendKey("USB");
          LED_Active(LED_R);
          break;
        // ----- INPUTs desconocidos -----
        default:
          sendKey("UNMAPPED");
          LED_Active(LED_R);
          break;
        }
      }
    }
    // Aviso en caso que que el modulo este bloqueado (apagado digital)
    if (Activo == false)
    {
      Serial.print("La placa esta apagada [");
      Serial.print(Activo);
      Serial.println("]");
    }
    IrReceiver.resume();
  }
}