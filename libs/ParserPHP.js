const fs = require('fs');
const parser = require('php-parser');

function inspectPHP(filePath) {
    const code = fs.readFileSync(filePath, 'utf-8');
    const phpParser = new parser.Engine({
        parser: {
            extractDoc: true,
            suppressErrors: true,
        },
    });

    const ast = phpParser.parseCode(code);

    const result = {
        "module": "",
        "classes": [],
        "functions": [],
        "variables": [],
    };

    function getFunctionParams(params) {
        return params.map(param => param.name ? param.name.name : '');
    }

    function traverse(node) {
        if (node.kind === 'class') {
            const classInfo = {
                name: node.name.name,
                functions: [],
                variables: [],
            };

            node.body.forEach(child => {
                if (child.kind === 'method') {
                    const functions = {
                        name: child.name.name,
                        params: getFunctionParams(child.arguments),
                    };
                    classInfo.functions.push(functions);
                } else if (child.kind === 'property') {
                    child.properties.forEach(prop => {
                        classInfo.variables.push(prop.name.name);
                    });
                }
            });

            result.classes.push(classInfo);
        } else if (node.kind === 'function') {
            const functionInfo = {
                name: node.name.name,
                params: getFunctionParams(node.arguments),
            };
            result.functions.push(functionInfo);
        } else if (node.kind === 'variable') {
            result.variables.push(node.name.name);
        }

        if (node.children) {
            node.children.forEach(traverse);
        }
    }

    ast.children.forEach(traverse);

    return result;
}

// Path ke file PHP
const filePath = process.argv[2];
const inspectionResult = inspectPHP(filePath);
console.log(JSON.stringify(inspectionResult, null, 2));