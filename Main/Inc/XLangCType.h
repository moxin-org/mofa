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

#ifndef XLANGCTYPEENUM_HPP
#define XLANGCTYPEENUM_HPP

#include <string>
#include <unordered_map>
#include <vector>
#include <sstream>
#include <typeinfo>
#include <cctype> // For std::isspace

namespace xMind {
    // Global map to hold enum mappings
    using EnumStringToValueMap = std::unordered_map<std::string, int>;
    using EnumValueToStringMap = std::unordered_map<int, std::string>;
    using EnumMappingPair = std::pair<EnumStringToValueMap, EnumValueToStringMap>;

    inline std::unordered_map<std::string, EnumMappingPair> globalEnumMap;

    // Helper function to trim whitespace from a string
    inline std::string trim(const std::string& str) {
        size_t first = str.find_first_not_of(' ');
        if (first == std::string::npos) return "";
        size_t last = str.find_last_not_of(' ');
        return str.substr(first, last - first + 1);
    }

    // RegisterEnum calculates each enum item's value based on the previous item
    template <typename EnumType>
    void RegisterEnum(const std::string& enumName, const std::string& enumStrList) {
        std::istringstream stream(enumStrList);
        std::string token;
        int currentValue = 0;  // Start at 0

        while (std::getline(stream, token, ',')) {
            auto trimmedToken = trim(token);
            auto pos = trimmedToken.find('=');
            std::string itemName;
            int value;

            if (pos != std::string::npos) {  // Item has an explicit value
                itemName = trim(trimmedToken.substr(0, pos));
                value = std::stoi(trim(trimmedToken.substr(pos + 1)));
            }
            else {  // Item's value is based on the previous item
                itemName = trimmedToken;
                value = currentValue;
            }

            currentValue = value + 1;  // Prepare for the next item

            // Store the mapping both ways: itemName <-> value
            globalEnumMap[enumName].first[itemName] = value;
            globalEnumMap[enumName].second[value] = itemName;
        }
    }

    template <typename EnumType>
    std::string EnumToStr(EnumType value) {
        std::string enumName = typeid(EnumType).name();
        int intValue = static_cast<int>(value);
        auto it = globalEnumMap[enumName].second.find(intValue);
        if (it != globalEnumMap[enumName].second.end()) {
            return it->second;
        }
        return "";  // Return empty string if the value is not found
    }

    template <typename EnumType>
    EnumType StrToEnum(const std::string& str) {
        std::string enumName = typeid(EnumType).name();
        auto it = globalEnumMap[enumName].first.find(str);
        if (it != globalEnumMap[enumName].first.end()) {
            return static_cast<EnumType>(it->second);
        }
        return static_cast<EnumType>(0);  // Return 0 if the string is not found
    }

    template <typename EnumType>
    std::vector<std::string> GetEnumNames() {
        std::string enumName = typeid(EnumType).name();
        std::vector<std::string> names;
        for (const auto& pair : globalEnumMap[enumName].first) {
            names.push_back(pair.first);
        }
        return names;
    }

    template <typename EnumType>
    std::string GetEnumListAsStr() {
        std::string enumName = typeid(EnumType).name();
        std::string result;
        for (const auto& pair : globalEnumMap[enumName].first) {
            result += pair.first;
            if (std::next(pair) != globalEnumMap[enumName].first.end()) {
                result += ", ";
            }
        }
        return result;
    }
}

#define ENUM_MAP(EnumName, ...) \
    enum class EnumName { __VA_ARGS__ }; \
    static const bool EnumName##Registered = (xMind::RegisterEnum<EnumName>(typeid(EnumName).name(), #__VA_ARGS__), true);

#endif // XLANGCTYPEENUM_HPP

