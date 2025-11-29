import fs from "fs/promises";
import path from "path";
import { exec } from "child_process";
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const PROJECT_ROOT = path.resolve("..");

const server = new Server(
  {
    name: "joes-burguer-tools",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Lista de ferramentas disponíveis
server.setRequestHandler("tools/list", async () => {
  return {
    tools: [
      {
        name: "listFiles",
        description: "Lista todos os arquivos do projeto",
        inputSchema: {
          type: "object",
          properties: {}
        }
      },
      {
        name: "readFile",
        description: "Lê um arquivo do projeto",
        inputSchema: {
          type: "object",
          properties: {
            file: { type: "string", description: "Caminho do arquivo" }
          },
          required: ["file"]
        }
      },
      {
        name: "writeFile",
        description: "Escreve em um arquivo do projeto",
        inputSchema: {
          type: "object",
          properties: {
            file: { type: "string", description: "Caminho do arquivo" },
            content: { type: "string", description: "Conteúdo" }
          },
          required: ["file", "content"]
        }
      },
      {
        name: "runCommand",
        description: "Executa comandos no projeto (npm, vite, node, etc)",
        inputSchema: {
          type: "object",
          properties: {
            command: { type: "string", description: "Comando a executar" }
          },
          required: ["command"]
        }
      }
    ]
  };
});

// Handler para executar as ferramentas
server.setRequestHandler("tools/call", async (request) => {
  const { name, arguments: args } = request.params;

  try {
    switch (name) {
      case "listFiles": {
        async function walk(dir) {
          const entries = await fs.readdir(dir, { withFileTypes: true });
          const files = await Promise.all(
            entries.map(async (entry) => {
              const full = path.join(dir, entry.name);
              if (entry.isDirectory()) {
                return walk(full);
              }
              return full;
            })
          );
          return files.flat();
        }

        const files = await walk(PROJECT_ROOT);
        return {
          content: [{
            type: "text",
            text: JSON.stringify({ files }, null, 2)
          }]
        };
      }

      case "readFile": {
        const fullPath = path.join(PROJECT_ROOT, args.file);
        const content = await fs.readFile(fullPath, "utf-8");
        return {
          content: [{
            type: "text",
            text: content
          }]
        };
      }

      case "writeFile": {
        const fullPath = path.join(PROJECT_ROOT, args.file);
        await fs.mkdir(path.dirname(fullPath), { recursive: true });
        await fs.writeFile(fullPath, args.content, "utf-8");
        return {
          content: [{
            type: "text",
            text: `✅ Arquivo atualizado: ${args.file}`
          }]
        };
      }

      case "runCommand": {
        return new Promise((resolve) => {
          exec(args.command, { cwd: PROJECT_ROOT }, (err, stdout, stderr) => {
            resolve({
              content: [{
                type: "text",
                text: JSON.stringify({
                  success: !err,
                  stdout,
                  stderr,
                  error: err?.message
                }, null, 2)
              }]
            });
          });
        });
      }

      default:
        throw new Error(`Ferramenta desconhecida: ${name}`);
    }
  } catch (error) {
    return {
      content: [{
        type: "text",
        text: `❌ Erro: ${error.message}`
      }],
      isError: true
    };
  }
});

// Iniciar servidor
const transport = new StdioServerTransport();
await server.connect(transport);

console.error("🚀 MCP Server iniciado - Joe's Burguer Tools");