from django.shortcuts import render, redirect


def home(request):
    return render(request, "detector/index.html")


def detect(request):
    if request.method == "POST":
        failed_login = int(request.POST.get("failed_login"))
        traffic = int(request.POST.get("traffic"))
        requests_count = int(request.POST.get("requests"))
        data = int(request.POST.get("data"))

        # 🔥 ATTACK LOGIC
        if failed_login > 10:
            attack = "Brute Force Attack"

        elif traffic > 1500 and requests_count > 600:
            attack = "DoS Attack"

        elif requests_count > 600 and traffic < 1000:
            attack = "Port Scan Attack"

        elif data > 200:
            attack = "Web Attack"

        else:
            attack = "Normal Activity"

        return redirect(f"/result/?attack={attack}")

    return render(request, "detector/detect.html")


def result(request):
    attack = request.GET.get("attack")
    return render(request, "detector/result.html", {"attack": attack})


def responce(request):
    attack = request.GET.get("attack")

    details = {
        "Normal Activity": {
            "cause": "The system is operating under normal conditions with low traffic, minimal failed login attempts, and balanced request handling. There are no signs of malicious behavior or suspicious patterns in the network.",
            "solution": "No action required. Continue monitoring the system regularly and maintain standard security practices such as updating software, using firewalls, and keeping logs."
        },

        "Brute Force Attack": {
            "cause": "This attack occurs when an attacker repeatedly tries different password combinations to gain unauthorized access. A high number of failed login attempts indicates automated scripts trying to break into accounts.",
            "solution": "Implement account lockout after multiple failed attempts, use strong passwords, enable two-factor authentication, and monitor login activity to prevent unauthorized access."
        },

        "DoS Attack": {
            "cause": "Denial of Service attack happens when the system is flooded with excessive traffic and requests, overwhelming the server and making it unavailable to legitimate users.",
            "solution": "Use firewalls and intrusion detection systems, limit the number of requests per user, implement load balancing, and block suspicious IP addresses generating high traffic."
        },

        "Port Scan Attack": {
            "cause": "Port scanning is performed by attackers to identify open ports and vulnerabilities in a system. A high number of requests with moderate traffic often indicates scanning activity.",
            "solution": "Close unused ports, use firewalls to block suspicious scanning attempts, enable intrusion detection systems, and regularly monitor network activity."
        },

        "Web Attack": {
            "cause": "Web attacks involve exploitation of web applications through abnormal data transfer, such as SQL injection or cross-site scripting. Large data transfer can indicate data manipulation or extraction attempts.",
            "solution": "Validate all user inputs, use secure coding practices, enable web application firewalls, and regularly update software to fix vulnerabilities."
        }
    }

    context = details.get(attack, {})

    return render(request, "detector/response.html", {
        "attack": attack,
        "cause": context.get("cause"),
        "solution": context.get("solution"),
    })
