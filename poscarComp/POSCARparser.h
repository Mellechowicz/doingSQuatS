#include <iostream>
#include <fstream>
#include <iomanip>

#include <string>

#include <array>
#include <vector>

#include <regex>
#include <numeric>

#include <stdexcept>
#include <limits>

template<typename T, class Matrix, class Vector>
class POSCARparser{
protected:
    std::ifstream strm;

    size_t system_size;
    T       multiplier;

    std::string comment, type;

    std::vector<std::string>       elements;
    std::vector<size_t>      elmement_count;

    Matrix                  basis;
    std::vector<Vector> positions;

// aux. variables
    size_t buffer, tmp_integer;
    std::string     tmp_string;

public:
/* ┏━╸┏━┓┏┓╻┏━┓╺┳╸┏━┓╻ ╻┏━╸╺┳╸┏━┓┏━┓┏━┓ *
 * ┃  ┃ ┃┃┗┫┗━┓ ┃ ┣┳┛┃ ┃┃   ┃ ┃ ┃┣┳┛┗━┓ *
 * ┗━╸┗━┛╹ ╹┗━┛ ╹ ╹┗╸┗━┛┗━╸ ╹ ┗━┛╹┗╸┗━┛ */
    POSCARparser() = delete;
    POSCARparser(const char _input[]):strm(_input),system_size(1U),buffer(0U){
        if (!strm.is_open()) {
            std::cerr << "Failed to open " << _input << std::endl;
        } else {
#ifdef _DEBUG            
            std::cout << "Opened " << _input << std::endl; 
#endif
        }
    }
    POSCARparser(const std::string& _input) : POSCARparser(_input.c_str()) {}

    static T read_next(const std::string& s, size_t& last_read){
        size_t buffer = 0U;
        T out = std::stod(s.substr(last_read),&buffer);
        last_read += buffer;
        return out;
    }
    
    static bool match_element(std::string& s, std::string& o){
        std::smatch m;
        std::regex mask("\\s*([A-Z][a-z]?)");
        if(std::regex_search(s,m,mask)){
            o = m[1];
            s = m.suffix();
            return true;
        }
        return false;
    }
    
    static bool match_count(std::string& s, size_t& n){
        std::smatch m;
        std::regex mask("\\s*([1-9][0-9]*)");
        if(std::regex_search(s,m,mask)){
            n = std::stoi(m[1]);
            s = m.suffix();
            return true;
        }
        return false;
    }

    bool parse(){ 
        std::string line;
        for(int i=0; getline(strm, line); ++i){
            if(positions.size() >= system_size) break;
            switch(i){
                case 0:
                    comment = line;
                    break;
                case 1:
                    multiplier = std::stod(line);
                    break;
                case 2:
                    buffer = 0U;
                    for(size_t j=0U; j<3U; ++j)
                        basis(j,0) = multiplier*read_next(line,buffer); 
                    break;
                case 3:
                    buffer = 0U;
                    for(size_t j=0U; j<3U; ++j)
                        basis(j,1) = multiplier*read_next(line,buffer); 
                    break;
                case 4:
                    buffer = 0U;
                    for(size_t j=0U; j<3U; ++j)
                        basis(j,2) = multiplier*read_next(line,buffer); 
                    break;
                case 5:
                    while(match_element(line,tmp_string)) elements.push_back(tmp_string);
                    break;
                case 6:
                    elmement_count.reserve(elements.size());
                    while(match_count(line,tmp_integer)) elmement_count.push_back(tmp_integer);
                    system_size = std::accumulate(elmement_count.begin(), elmement_count.end(), 0U);
                    positions.reserve(system_size);
                    break;
                case 7:
                    type = line;
                    type.erase(remove_if(type.begin(), type.end(), isspace), type.end());
                    std::transform(type.begin(), type.end(),type.begin(), ::tolower);
                    break;
                default:
                    Vector position;
                    buffer = 0U;
                    for(size_t j=0U; j<3U; ++j)
                        position(j) = read_next(line,buffer); 
                    positions.push_back(position);
                    break;
            }
        }
        if(type[0] == 'c' || type[0] == 'k'){
            for(auto& pos : positions)
                pos = basis.i()*pos;
        }
        return true;
    }

public:
    const std::string&               get_comment()       const{return        comment;}
    const Matrix&                    get_basis()         const{return          basis;}
    const std::vector<std::string>&  get_elements()      const{return       elements;}
    const std::vector<size_t>&       get_element_count() const{return elmement_count;}
    const std::vector<Vector>&       get_positions()     const{return      positions;}
    const size_t&                    get_system_size()   const{return    system_size;}

    friend std::ostream& operator<<(std::ostream& output, const POSCARparser<T,Matrix,Vector>& parser) {
        auto space = std::setw(std::numeric_limits<T>::digits10 + 5);
        output<< std::fixed;
        output<< std::showpoint;
        output<< std::setprecision(std::numeric_limits<T>::digits10 + 1); 
        output<< std::right;
        output<<parser.get_comment()<<std::endl;
        output<<"1.0"<<std::endl;
        for(size_t i=0U; i<3; ++i){
            output<<space<<parser.get_basis()(0,i)<<"  "<<space<<parser.get_basis()(1,i)<<"  "<<space<<parser.get_basis()(2,i)<<std::endl;
        }
        for(const auto& e : parser.get_elements()){
            output<<e<<" ";
        }
        output<<std::endl;
        for(const auto& n : parser.get_element_count() ){
            output<<n<<" ";
        }
        output<<std::endl;
        output<<"Direct"<<std::endl;
        for(const auto& pos : parser.get_positions()){
            output<<space<<pos(0)<<"  "<<space<<pos(1)<<"  "<<space<<pos(2)<<std::endl;
        }
        return output;
    }
};
