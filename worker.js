export default {
  async fetch(request) {

    const cors = {
      "Access-Control-Allow-Origin": "https://maiconbr15.github.io",
      "Access-Control-Allow-Methods": "GET, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
      "Cache-Control": "no-store"
    };

    if (request.method === "OPTIONS") {
      return new Response(null, {
        status: 204,
        headers: cors
      });
    }

    const requestUrl = new URL(request.url);
    const target = requestUrl.searchParams.get("url");

    if (!target) {
      return new Response("URL não informada.", {
        status: 400,
        headers: cors
      });
    }

    let consulta;

    try {
      consulta = new URL(target);
    } catch {
      return new Response("URL inválida.", {
        status: 400,
        headers: cors
      });
    }

    // O proxy só pode acessar este domínio.
    if (
      consulta.protocol !== "https:" ||
      consulta.hostname !== "consultas.gonzalesdev.shop"
    ) {
      return new Response("Domínio não permitido.", {
        status: 403,
        headers: cors
      });
    }

    try {

      const resposta = await fetch(consulta.toString(), {
        method: "GET",
        redirect: "follow",

        headers: {
          "Accept": "text/html,application/xhtml+xml",
          "User-Agent":
            "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 Version/18.0 Mobile/15E148 Safari/604.1"
        }
      });

      const html = await resposta.text();

      return new Response(html, {
        status: resposta.status,

        headers: {
          ...cors,
          "Content-Type": "text/html; charset=UTF-8"
        }
      });

    } catch (erro) {

      return new Response(
        "Não foi possível acessar a consulta.",
        {
          status: 502,
          headers: cors
        }
      );

    }
  }
};