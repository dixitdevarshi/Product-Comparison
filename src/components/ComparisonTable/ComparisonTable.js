import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './ComparisonTable.css';

const ComparisonTable = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const { items } = location.state || {};

    if (!items) {
        return (
            <div className="comparison-table">
                <h2>No items to compare</h2>
                <button onClick={() => navigate('/products-comparison')}>Go Back</button>
            </div>
        );
    }

    const productSpecs = {
        item1: { name: items.item1, spec1: 'Spec A1', spec2: 'Spec B1' },
        item2: { name: items.item2, spec1: 'Spec A2', spec2: 'Spec B2' }
    };

    return (
        <div className="comparison-table">
            <h2>Comparison Table</h2>
            <table>
                <thead>
                    <tr>
                        <th>Specification</th>
                        <th>{productSpecs.item1.name}</th>
                        <th>{productSpecs.item2.name}</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Spec 1</td>
                        <td>{productSpecs.item1.spec1}</td>
                        <td>{productSpecs.item2.spec1}</td>
                    </tr>
                    <tr>
                        <td>Spec 2</td>
                        <td>{productSpecs.item1.spec2}</td>
                        <td>{productSpecs.item2.spec2}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    );
};

export default ComparisonTable;
