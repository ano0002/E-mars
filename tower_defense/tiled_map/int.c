int pow(int val,int exp){
    int i;

    if (exp == 0)
    {
        return 1;
    }
    else
    {
        return val * pow(val, exp - 1);
    }
}