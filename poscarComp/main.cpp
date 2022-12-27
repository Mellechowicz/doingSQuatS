#include <iostream>
#include "POSCARparser.h"

#include <armadillo>
#include <xtalcomp/xtalcomp.h>

struct CellData{
    XcMatrix cell;
    std::vector<unsigned> types;
    std::vector<XcVector> positions;
};

template<typename T, class Matrix, class Vector>
CellData translate_to_Xc(const POSCARparser<T,Matrix,Vector>& parser){
    CellData from_POSCAR;
    
    const auto& basis = parser.get_basis();
    from_POSCAR.cell = XcMatrix(basis(0,0),basis(1,0),basis(2,0),basis(0,1),basis(1,1),basis(1,2),basis(0,2),basis(1,2),basis(2,2));

    from_POSCAR.positions.reserve(parser.get_system_size());

    for(const auto& pos : parser.get_positions())
        from_POSCAR.positions.push_back(XcVector(pos(0),pos(1),pos(2)));

    from_POSCAR.types.reserve(parser.get_system_size());
    size_t idx = 1;
    for(const size_t& count : parser.get_element_count()){
        for(size_t i=0U; i< count; ++i){
            from_POSCAR.types.push_back(idx);
        }
        ++idx;
    }

    return from_POSCAR;
}

bool test_two_cells(const CellData& one, const CellData& two){
  bool match = XtalComp::compare(one.cell, one.types, one.positions,
                                 two.cell, two.types, two.positions,
                                 NULL, 0.10, 5.00);

  if (!match)
    return false;

  return true;
}

template<typename T, class Matrix, class Vector>
bool compare(const POSCARparser<T,Matrix,Vector>& one, const POSCARparser<T,Matrix,Vector>& two){
    auto Xc_one = translate_to_Xc(one);
    auto Xc_two = translate_to_Xc(two);
    return test_two_cells(Xc_one,Xc_two);
}

int main(int argc, char** argv){
    for(int i = 1; i<argc-1; i+=2){
        POSCARparser<double,arma::mat::fixed<3,3>,arma::vec::fixed<3>> one(argv[i]);
        POSCARparser<double,arma::mat::fixed<3,3>,arma::vec::fixed<3>> two(argv[i+1]);
        one.parse();
        two.parse();
        int result = compare(one,two);
#ifdef _DEBUG
        std::cout<<one<<std::endl;
        std::cout<<two<<std::endl;
#endif
        std::cout<<result<<std::endl;
    }
    return 0;
}
