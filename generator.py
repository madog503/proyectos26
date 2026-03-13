#!/usr/bin/env python3
"""Generador de artículos técnicos de diagnóstico automotriz en HTML."""

from __future__ import annotations

import argparse
from pathlib import Path
from textwrap import dedent

TOPICS = {
    "P0300: Fallos de encendido aleatorios": {
        "problem_meaning": (
            "El código P0300 indica que la unidad de control detecta combustiones irregulares "
            "en uno o varios cilindros sin un patrón fijo. En términos prácticos, el motor no "
            "quema la mezcla aire-combustible de forma uniforme, lo que provoca vibraciones, "
            "pérdida de potencia y aumento de emisiones."
        ),
        "symptoms": [
            "Ralentí inestable con temblores perceptibles en cabina.",
            "Pérdida de fuerza al acelerar, especialmente en subidas.",
            "Luz de Check Engine fija o parpadeando en cargas altas.",
            "Aumento del consumo de combustible y olor a gasolina sin quemar.",
            "Tirones al iniciar la marcha o al mantener velocidad constante.",
        ],
        "causes": [
            "Bujías gastadas, contaminadas o con calibración incorrecta.",
            "Bobinas de encendido con fuga interna o baja energía de chispa.",
            "Inyectores con patrón de pulverización deficiente.",
            "Fugas de vacío en mangueras, múltiple o empaque del cuerpo de aceleración.",
            "Baja presión de combustible por filtro restringido o bomba débil.",
        ],
        "diagnosis": [
            "Leer códigos con escáner OBD2 y revisar freeze frame para conocer carga, rpm y temperatura cuando ocurrió la falla.",
            "Inspeccionar bujías y bobinas: buscar electrodos erosionados, grietas o rastros de carbonización externa.",
            "Medir presión de combustible y comparar con especificación de fábrica en ralentí y bajo aceleración.",
            "Revisar correcciones de combustible (STFT/LTFT): valores muy positivos sugieren mezcla pobre por aire falso o falta de combustible.",
            "Realizar prueba de humo en admisión y prueba de balance de inyectores para confirmar fugas o caudal desigual.",
        ],
        "solutions": [
            "Sustituir bujías por el grado térmico recomendado y torquear correctamente.",
            "Cambiar bobinas defectuosas y revisar conectores con falso contacto.",
            "Lavar o reemplazar inyectores según resultado de prueba de caudal.",
            "Corregir fugas de vacío y reemplazar empaques endurecidos.",
            "Restaurar presión de combustible (filtro, bomba o regulador según diagnóstico).",
        ],
        "driving": (
            "Conducir periodos cortos puede ser posible si la falla es leve, pero no es recomendable. "
            "Un misfire sostenido sobrecalienta el catalizador y puede dañarlo en pocos kilómetros. "
            "Si la luz de motor parpadea, lo más seguro es detener el vehículo y remolcarlo al taller."
        ),
        "shop_experience": (
            "En un sedán 1.8 llegó una queja de vibración solo con aire acondicionado encendido. "
            "El escáner mostraba P0300 sin código de cilindro específico. Tras revisar datos en vivo, "
            "observamos corrección positiva en banco único y una caída leve de presión al acelerar. "
            "El problema final fue un filtro de combustible parcialmente obstruido combinado con dos bujías "
            "fuera de vida útil. Con mantenimiento completo, el ralentí volvió a la normalidad."
        ),
        "mechanic_tip": (
            "Cuando cambies bujías en motores modernos, evita aplicar grasa excesiva en roscas y respeta el torque. "
            "Un apriete incorrecto altera la transferencia térmica y acorta su duración."
        ),
        "warning": (
            "No borres códigos sin registrar datos previos. Perderás evidencia clave del momento exacto en que se produjo la falla."
        ),
        "conclusion": (
            "El P0300 no se resuelve cambiando piezas al azar. Un diagnóstico por etapas, apoyado en datos reales, "
            "permite reparar con precisión, proteger el catalizador y recuperar consumo y rendimiento."
        ),
    },
    "Sobrecalentamiento del motor en tráfico": {
        "problem_meaning": (
            "El sobrecalentamiento aparece cuando el sistema de enfriamiento no logra evacuar el calor que genera el motor. "
            "En tráfico lento el flujo de aire natural baja, por lo que ventiladores, radiador y circulación de refrigerante "
            "deben trabajar al 100 %. Si uno de estos elementos falla, la temperatura sube rápidamente."
        ),
        "symptoms": [
            "Indicador de temperatura acercándose a zona roja en ciudad.",
            "Ventilador encendiendo tarde o trabajando de forma intermitente.",
            "Olor dulce a refrigerante y posible vapor en cofre.",
            "Calefacción interna sin rendimiento por falta de circulación.",
            "Pérdida de potencia cuando la ECU entra en modo de protección.",
        ],
        "causes": [
            "Nivel bajo de refrigerante por fuga en mangueras, radiador o depósito.",
            "Termostato atascado que limita el paso hacia el radiador.",
            "Electroventilador dañado o relevador/fusible defectuoso.",
            "Bomba de agua con impulsor desgastado o juego excesivo.",
            "Radiador internamente obstruido por corrosión o uso de agua sin aditivos.",
        ],
        "diagnosis": [
            "Verificar nivel y estado del refrigerante con motor frío; buscar aceite o sedimentos anormales.",
            "Presurizar el sistema para localizar fugas externas sin necesidad de sobrecalentar el motor.",
            "Confirmar apertura del termostato observando temperatura de mangueras superior e inferior.",
            "Activar ventiladores desde escáner o prueba directa para validar motor, relevador y alimentación.",
            "Medir diferencia de temperatura en entrada/salida de radiador para detectar restricción de flujo.",
        ],
        "solutions": [
            "Reparar fugas y purgar correctamente para eliminar bolsas de aire.",
            "Sustituir termostato y tapa de radiador cuando no sostienen presión especificada.",
            "Cambiar ventilador, relevadores o sensores de temperatura según resultado eléctrico.",
            "Reemplazar bomba de agua si existe ruido, fuga por retén o baja circulación.",
            "Realizar limpieza profesional o cambio de radiador en casos de obstrucción severa.",
        ],
        "driving": (
            "No se debe seguir conduciendo con temperatura alta. Cada minuto de sobrecalentamiento incrementa el riesgo "
            "de deformar la culata, dañar junta de cabeza y contaminar aceite. Si la aguja supera el rango normal, "
            "apaga el aire acondicionado, enciende calefacción y detente en un lugar seguro cuanto antes."
        ),
        "shop_experience": (
            "Una SUV llegaba siempre caliente después de 20 minutos en embotellamiento, pero en carretera funcionaba bien. "
            "El cliente ya había cambiado termostato sin éxito. Encontramos que el ventilador de baja velocidad no activaba "
            "por un relevador sulfatado; solo entraba la velocidad alta cuando la temperatura ya era crítica. "
            "Con reemplazo del relevador y limpieza de conectores, la temperatura quedó estable."
        ),
        "mechanic_tip": (
            "Usa siempre refrigerante de especificación correcta. Mezclar formulaciones incompatibles genera lodos que reducen "
            "el intercambio térmico y tapan conductos finos."
        ),
        "warning": (
            "Nunca abras la tapa del radiador con el motor caliente; la presión puede expulsar líquido a alta temperatura y provocar quemaduras graves."
        ),
        "conclusion": (
            "El sobrecalentamiento casi siempre avisa antes de causar daño mayor. Detectar fugas, revisar ventilación y mantener "
            "el sistema limpio evita reparaciones costosas como rectificación de culata o reconstrucción de motor."
        ),
    },
    "Ruido metálico al frenar": {
        "problem_meaning": (
            "Un ruido metálico al frenar suele indicar contacto anormal entre componentes del sistema de frenos. "
            "Puede ser desde un testigo de desgaste tocando el disco hasta piezas flojas que vibran. "
            "No es solo un tema de confort: también puede comprometer distancia de frenado y seguridad."
        ),
        "symptoms": [
            "Chirrido o roce metálico al pisar el pedal de freno.",
            "Vibración en volante o pedal durante frenadas medias.",
            "Mayor distancia para detener el vehículo.",
            "Desgaste irregular en una o más pastillas.",
            "Rines con acumulación excesiva de polvo oscuro de freno.",
        ],
        "causes": [
            "Pastillas al límite de espesor con placa metálica en contacto con disco.",
            "Discos rayados, cristalizados o fuera de tolerancia por alabeo.",
            "Pernos guía del cáliper sin lubricación o trabados.",
            "Láminas anti-ruido mal instaladas o ausentes.",
            "Material de fricción de baja calidad incompatible con el uso del vehículo.",
        ],
        "diagnosis": [
            "Retirar ruedas y medir espesor de pastillas y discos con herramienta calibrada.",
            "Inspeccionar superficie del disco para detectar surcos profundos o zonas azuladas por sobrecalentamiento.",
            "Comprobar libre movimiento de pernos guía y pistón del cáliper.",
            "Verificar torque de ruedas, soporte de cáliper y estado de láminas anti-ruido.",
            "Realizar prueba dinámica controlada para confirmar si el ruido aparece en frío, caliente o solo en frenadas largas.",
        ],
        "solutions": [
            "Reemplazar pastillas y discos cuando superan límites de desgaste.",
            "Rectificar discos solo si el espesor remanente lo permite según fabricante.",
            "Limpiar y lubricar pernos guía con grasa de alta temperatura específica para frenos.",
            "Instalar herrajes anti-ruido nuevos en cada servicio de pastillas.",
            "Asentar correctamente las pastillas nuevas con una secuencia progresiva de frenadas.",
        ],
        "driving": (
            "Si el ruido es reciente y leve, puede desplazarse el auto solo para llegar al taller cercano. "
            "Si se acompaña de vibración fuerte, pérdida de frenado o jaloneo, no conviene seguir circulando. "
            "El riesgo de daño mayor en disco y cáliper aumenta rápidamente."
        ),
        "shop_experience": (
            "Atendimos un compacto con ruido metálico después de cambiar pastillas en otro lugar. "
            "La causa no eran las pastillas nuevas, sino la falta de láminas anti-ruido y pernos secos. "
            "Eso provocaba vibración y desgaste inclinado. Tras reinstalar herrajes, lubricar y asentar el conjunto, "
            "el sistema recuperó frenada silenciosa y estable."
        ),
        "mechanic_tip": (
            "No uses grasa común en componentes de freno. Debe ser una formulación resistente a altas temperaturas "
            "y compatible con gomas para no dañar retenes."
        ),
        "warning": (
            "Ignorar ruidos en frenos puede terminar en daño de disco y pérdida de eficiencia de frenado. Ante cualquier cambio de sonido, revisa de inmediato."
        ),
        "conclusion": (
            "El ruido metálico al frenar casi siempre tiene causa mecánica identificable. Con inspección precisa y piezas de calidad, "
            "se corrige el sonido y, sobre todo, se mantiene la seguridad del vehículo."
        ),
    },
}


def html_list(items: list[str]) -> str:
    return "\n".join(f"    <li>{item}</li>" for item in items)


def generate_article_html(title: str) -> str:
    if title not in TOPICS:
        allowed = "\n".join(f"- {name}" for name in TOPICS)
        raise ValueError(f"Título no soportado. Opciones disponibles:\n{allowed}")

    data = TOPICS[title]
    intro = (
        f"<p>{title} es una consulta frecuente en diagnóstico automotriz porque suele aparecer de forma "
        "progresiva y confundirse con otras fallas. En este artículo vamos a revisar cómo interpretarlo "
        "desde taller: qué síntomas mirar primero, qué pruebas dan información útil y cómo priorizar una "
        "reparación efectiva sin cambiar piezas innecesarias. El objetivo es que puedas diferenciar una "
        "avería real de una condición secundaria, algo clave para no disparar costos en refacciones ni "
        "alargar tiempos de inmovilización del vehículo.</p>"
    )

    causes_context = (
        "<p>En muchos casos se presentan dos o más causas al mismo tiempo. Por eso no conviene asumir que "
        "la primera pieza con desgaste es la responsable total. La práctica profesional es validar la causa "
        "raíz con mediciones y luego revisar qué componentes resultaron afectados como consecuencia del problema "
        "principal.</p>"
    )

    diagnosis_context = (
        "<p>El diagnóstico técnico debe seguir una secuencia lógica: primero confirmar el síntoma, después "
        "obtener datos objetivos y finalmente intervenir. Saltarse etapas suele generar reemplazos innecesarios. "
        "Un buen criterio es comparar siempre el dato medido contra especificación del fabricante y repetir la "
        "prueba tras cada corrección para confirmar que el problema desapareció.</p>"
    )

    solution_context = (
        "<p>Cuando se realiza la reparación, es recomendable cerrar el trabajo con una verificación completa: "
        "borrar códigos o adaptaciones si aplica, efectuar prueba de ruta y revisar que no existan fugas, "
        "ruidos o parámetros fuera de rango. Esta etapa final evita regresos a taller y confirma que la solución "
        "es estable en condiciones reales de uso.</p>"
    )

    meaning_context = (
        "<p>Desde el punto de vista técnico, este tipo de falla también debe leerse en contexto: kilometraje, calidad "
        "de mantenimiento previo, estilo de conducción y condiciones ambientales. Un mismo síntoma puede tener "
        "orígenes distintos en ciudad, carretera o climas extremos, por eso el historial del vehículo es parte "
        "del diagnóstico y no un dato secundario.</p>"
    )

    conclusion_context = (
        "<p>Como regla general, cuanto antes se atiende una falla de este tipo, menor es el impacto económico. "
        "Postergar el diagnóstico suele convertir una reparación puntual en una intervención mayor que afecta "
        "tiempo de operación del vehículo, consumo de combustible y seguridad de manejo. También conviene "
        "registrar el servicio realizado y los valores medidos, porque ese historial facilita diagnósticos "
        "futuros y ayuda a detectar tendencias de desgaste antes de que se conviertan en averías críticas.</p>"
    )

    return dedent(
        f"""\
        <h1>{title}</h1>
        {intro}

        <h2>¿Qué significa este problema?</h2>
        <p>{data['problem_meaning']}</p>
        {meaning_context}

        <h2>Síntomas más comunes</h2>
        <ul>
        {html_list(data['symptoms'])}
        </ul>

        <h2>Causas más comunes</h2>
        <ul>
        {html_list(data['causes'])}
        </ul>
        {causes_context}

        <h2>Cómo diagnosticar el problema</h2>
        <ol>
        {html_list(data['diagnosis'])}
        </ol>
        {diagnosis_context}

        <h2>Cómo solucionar el problema</h2>
        <ul>
        {html_list(data['solutions'])}
        </ul>
        {solution_context}

        <h2>¿Se puede seguir conduciendo con este problema?</h2>
        <p>{data['driving']}</p>

        <h2>Experiencia real en taller</h2>
        <p>{data['shop_experience']}</p>

        <h2>Consejo de mecánico</h2>
        <p>{data['mechanic_tip']}</p>

        <h2>Advertencia</h2>
        <p>{data['warning']}</p>

        <h2>Conclusión</h2>
        <p>{data['conclusion']}</p>
        {conclusion_context}
        """
    ).strip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Genera artículos HTML en español para un blog técnico automotriz."
    )
    parser.add_argument(
        "--title",
        help="Título exacto del artículo a generar.",
    )
    parser.add_argument(
        "--list-topics",
        action="store_true",
        help="Muestra la lista predefinida de títulos disponibles.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Genera un archivo HTML por cada título predefinido.",
    )
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Carpeta destino para archivos generados con --all.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.list_topics:
        for topic in TOPICS:
            print(topic)
        return 0

    if args.all:
        out_dir = Path(args.output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        for topic in TOPICS:
            file_name = (
                topic.lower()
                .replace(":", "")
                .replace("¿", "")
                .replace("?", "")
                .replace(" ", "-")
            )
            path = out_dir / f"{file_name}.html"
            path.write_text(generate_article_html(topic), encoding="utf-8")
            print(f"Generado: {path}")
        return 0

    if not args.title:
        raise SystemExit("Debes usar --title, --all o --list-topics.")

    print(generate_article_html(args.title))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
