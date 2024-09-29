/*
Copyright (C) 2024 The XLang Foundation

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

#include "XMindCmd.h"
#include <iostream>
#include <regex>
#include <string>
#include <vector>
#include <algorithm>
#include <cctype>
#include "Callable.h"

namespace xMind
{
    // Helper function to trim leading and trailing spaces from a string
    static std::string trimSpace(const std::string& str) {
        if (str.empty()) return str; // Handle empty string case

        auto start = str.begin();
        while (start != str.end() && std::isspace(*start)) {
            start++;
        }

        auto end = str.end();
        do {
            end--;
        } while (std::distance(start, end) > 0 && std::isspace(*end));

        return std::string(start, end + 1);
    }

    // Helper function to remove surrounding quotes from a string
    static std::string removeQuotes(const std::string& str) {
        if (str.size() >= 2) {
            if ((str.front() == '"' && str.back() == '"') || (str.front() == '\'' && str.back() == '\'')) {
                return str.substr(1, str.size() - 2);
            }
        }
        return str;
    }

    // Function to parse and return a list of commands found in the input string
    //also change the input to remove command parts
    std::vector<Command> parseCmd(std::string& input) {
        std::vector<Command> commands;

        // Define the regular expression to match the entire pattern, allowing spaces around '{', 'xmind-cmd', and ':'
        std::regex fullPattern(R"(\{\s*xmind-cmd\s*:\s*(.+?)\s*\})");
        std::smatch match;

        // Continue searching and erasing matched commands
        while (std::regex_search(input, match, fullPattern)) {
            std::string cmdsPart = match[1].str();  // Extract the commands part

            // Define the regular expression to match each command with or without parameters
            std::regex cmdPattern(R"((\w+)\s*\(([^)]*)\)\s*|(\w+))");
            std::sregex_iterator cmdIt(cmdsPart.begin(), cmdsPart.end(), cmdPattern);
            std::sregex_iterator end;

            // Iterate through each command in the matched section
            while (cmdIt != end) {
                Command cmd;
                if ((*cmdIt)[1].matched) {
                    // Command with parameters
                    cmd.name = (*cmdIt)[1].str();
                    std::string paramsStr = (*cmdIt)[2].str();

                    // Split parameters by commas, taking care of floats, integers, strings, and quoted strings
                    std::regex paramPattern(R"(([^,]+))");
                    std::sregex_token_iterator paramIt(paramsStr.begin(), paramsStr.end(), paramPattern);
                    std::sregex_token_iterator paramEnd;
                    for (; paramIt != paramEnd; ++paramIt) {
                        std::string trimmedParam = trimSpace(paramIt->str());
                        trimmedParam = removeQuotes(trimmedParam);  // Remove surrounding quotes if present
                        if (!trimmedParam.empty()) {
                            cmd.params.push_back(trimmedParam);  // Add parameter after trimming and removing quotes
                        }
                    }
                }
                else if ((*cmdIt)[3].matched) {
                    // Command without parameters (just a name)
                    cmd.name = (*cmdIt)[3].str();
                }

                commands.push_back(cmd);
                ++cmdIt;
            }

            // Erase the matched section from the input string
            input.erase(match.position(), match.length());
        }

        return commands;
    }

    std::vector<Command> parseCmd0(const std::string& input) {
        std::vector<Command> commands;

        // Define the regular expression to match the entire pattern, allowing spaces around '{', 'xmind-cmd', and ':'
        std::regex fullPattern(R"(\{\s*xmind-cmd\s*:\s*(.+?)\s*\})");
        std::smatch match;

        auto it = input.cbegin();
        while (std::regex_search(it, input.cend(), match, fullPattern)) {
            std::string cmdsPart = match[1].str();  // Extract the commands part

            // Define the regular expression to match each command with or without parameters
            std::regex cmdPattern(R"((\w+)\s*\(([^)]*)\)\s*|(\w+))");
            std::sregex_iterator cmdIt(cmdsPart.begin(), cmdsPart.end(), cmdPattern);
            std::sregex_iterator end;

            while (cmdIt != end) {
                Command cmd;
                if ((*cmdIt)[1].matched) {
                    // Command with parameters
                    cmd.name = (*cmdIt)[1].str();
                    std::string paramsStr = (*cmdIt)[2].str();

                    // Split parameters by commas, taking care of floats, integers, strings, and quoted strings
                    std::regex paramPattern(R"(([^,]+))");
                    std::sregex_token_iterator paramIt(paramsStr.begin(), paramsStr.end(), paramPattern);
                    std::sregex_token_iterator paramEnd;
                    for (; paramIt != paramEnd; ++paramIt) {
                        std::string trimmedParam = trimSpace(paramIt->str());
                        trimmedParam = removeQuotes(trimmedParam);  // Remove surrounding quotes if present
                        if (!trimmedParam.empty()) {
                            cmd.params.push_back(trimmedParam);  // Add parameter after trimming and removing quotes
                        }
                    }
                }
                else if ((*cmdIt)[3].matched) {
                    // Command without parameters (just a name)
                    cmd.name = (*cmdIt)[3].str();
                }

                commands.push_back(cmd);
                ++cmdIt;
            }

            it = match.suffix().first;  // Move to the next part of the input string after the matched command
        }

        return commands;
    }

    void executeCmd(Callable* callable, Command& cmd)
    {
		// Execute the command here
        if (cmd.name == "BreakConnection")
        {
			callable->BreakConnection(cmd.params[0]);
        }
    }
}