#include "lest/lest.hpp"

using namespace std;

const lest::test specification[] =
{
    CASE( "Empty string has length zero (succeed)" )
    {
        EXPECT( 0 == string(  ).length() );
        EXPECT( 0 == string("").length() );
    },
/*
    CASE( "Text compares lexically (fail)" )
    {
        EXPECT( string("hello") > string("world") );
    },

    CASE( "Unexpected exception is reported" )
    {
        EXPECT( (throw std::runtime_error("surprise!"), true) );
    },
*/
    CASE( "Unspecified expected exception is captured" )
    {
        EXPECT_THROWS( throw std::runtime_error("surprise!") );
    },

    CASE( "Specified expected exception is captured" )
    {
        EXPECT_THROWS_AS( throw std::bad_alloc(), std::bad_alloc );
    },
/*
    CASE( "Expected exception is reported missing" )
    {
        EXPECT_THROWS( true );
    },

    CASE( "Specific expected exception is reported missing" )
    {
        EXPECT_THROWS_AS( true, std::runtime_error );
    },*/
};

int main( int argc, char * argv[] )
{
    return lest::run( specification, argc, argv );
}
