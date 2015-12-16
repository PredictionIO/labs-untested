// g++ -std=c++14 -O3 utm_extractor.cpp -o utm_extractor
#include <iostream>
#include <fstream>
#include <string>
#include <unordered_set>
#include <vector>
#include <sstream>

int main(int argc, char **argv)
{
    std::ios_base::sync_with_stdio(false);
    if (argc != 5) {
        std::cerr << argv[0] << " [packed_input.csv] [culumn_num] [utm_hashes.csv] [output.csv]\n\n";
        return 1;
    }

    typedef int64_t utmType;
    std::unordered_set<utmType> hashes_set;
    std::ifstream hashes(argv[3]);
    if (hashes.fail()) {
        std::cerr << "Unable to read from " << argv[3] << "\n";
        return 2;
    }
    std::string line;
    while (std::getline(hashes, line)) {
        hashes_set.insert(std::stoul(line));
    }
    hashes.close();
    std::vector<utmType> hashes_vec(hashes_set.begin(), hashes_set.end());
    hashes_set.clear();

    const int columnNum = std::stoi(argv[2]);

    std::ifstream input(argv[1]);
    if (input.fail()) {
        std::cerr << "Unable to read from " << argv[0] << "\n";
        return 3;
    }
    std::ofstream output(argv[4]);
    if (input.fail()) {
        std::cerr << "Unable to write to " << argv[4] << "\n";
        return 4;
    }
    while (std::getline(input, line)) {
        utmType tag = -1;
        std::istringstream lbuf(line);
        for (int i = 0; ; ++i) {
            std::string cell;
            std::getline(lbuf, cell, ',');
            if (!lbuf) {
                break;
            }
            if (i != columnNum) {
                output << cell << ',';
            } else {
                tag = std::stoul(cell);
            }
        }
        for (auto i = hashes_vec.cbegin(), e = hashes_vec.cend(); i != e; ++i) {
            output << (tag == *i);
            auto c = i;
            ++c;
            if (c != e) {
                output << ',';
            }
        }
        output << "\n";
    }

    return 0;
}
