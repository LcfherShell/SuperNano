const acorn = require('acorn');
const fs = require('fs');

function analyzeFile(filePath) {
    const code = fs.readFileSync(filePath, 'utf-8');
    const syntax = acorn.parse(code, { ecmaVersion: 2020, sourceType: 'module' });


    const result = {
        "module": "",
        "classes": [],
        "functions": [],
        "variables": [],
    }

    // Recursive function to traverse AST nodes
    function walk(node) {
        function extractParameters(params) {
            return params.map(param => param?.name || param?.params || '');
        }    
        if (node.type === 'ClassDeclaration' && node.id) {
            const classInfo = {
                name: node.id.name,
                variables: [],
                functions: []
            };
            
            // Collect variables and methods within the class body
            node.body.body.forEach(member => {
                if (member.type === 'MethodDefinition' && member.key) {
                    if (member.key.name) {
                        const methodName = member.key.name;
                        const methodType = member.static ? 'static' : 'instance';
                        var parameters
                        if (member.value.params){
                            parameters = extractParameters(member.value.params)
                        }else{
                            parameters = [""]
                        }
                        classInfo.functions.push({ name: `${methodName}`, params: parameters, type: methodType });
                    }
                } else if (member.type === 'ClassProperty' && member.key) {
                    if (member.key.name) {
                        classInfo.variables.push(member.key.name);
                    }
                }
            });

            result.classes.push(classInfo);
        } else if (node.type === 'FunctionDeclaration' && node.id) {
            if (node.id?.name!=undefined){
                var parameters
                if (node.params){
                    parameters = extractParameters(node.params);
                }
                result.functions.push({
                    name: `${node.id.name}`,
                    params: parameters
                });
            }
        }else if (node.type === 'FunctionExpression' || node.type === 'ArrowFunctionExpression') { 
            if (node.id?.name!=undefined){
                var parameters
                if (node.params){
                    parameters = extractParameters(node.params);
                }else{
                    parameters = ""
                }
                result.functions.push({
                    name: `${node.id.name}`,
                    params: parameters
                });
            }
        }else if (node.type === 'MethodDefinition' && node.key) {
            if (node.id?.name!=undefined) {
                var parameters
                if (node.params){
                    parameters = extractParameters(node.params);
                }else{
                    parameters = ""
                }
                result.functions.push({
                    name: `${node.id.name}`,
                    params: parameters
                });
            }
        }else if (node.type === 'VariableDeclarator' && node.id) {
            if (node.id?.name!=undefined){
                result.variables.push(node.id.name);
            }
        }
        
        // Traverse child nodes
        for (let key in node) {
            if (node[key] && typeof node[key] === 'object') {
                walk(node[key]);
            }
        }
    }
    // Start walking from the top-level nodes
    walk(syntax);
    //const functionMap = new Map();
    //functions.forEach(func => {
        //if (functionMap.has(func.name)) {
        //    func.type = 'class method';
        //} else {
        //    func.type = 'function';
        //}
    //});
    return result;//JSON.stringify({"classes":classes, "functions":functions, "variables":variables });
}



// Contoh penggunaan
const filePath = process.argv[2];
const inspectionResult = analyzeFile(filePath);
console.log(JSON.stringify(inspectionResult, null, 2));